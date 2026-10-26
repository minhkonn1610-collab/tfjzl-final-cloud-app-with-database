from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Course, Enrollment, Learner, Question, Submission


def course_list(request):
    courses = Course.objects.order_by("name")
    return render(request, "onlinecourse/course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
    )


@login_required
def exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.prefetch_related("choices").all()
    return render(
        request,
        "onlinecourse/exam.html",
        {"course": course, "questions": questions},
    )


def _get_enrollment_for_user(user, course):
    learner, _ = Learner.objects.get_or_create(
        user=user,
        defaults={"full_name": user.get_full_name() or user.get_username()},
    )
    enrollment, _ = Enrollment.objects.get_or_create(learner=learner, course=course)
    return enrollment


@login_required
def submit(request, course_id):
    if request.method != "POST":
        return redirect("onlinecourse:exam", course_id=course_id)

    course = get_object_or_404(Course, pk=course_id)
    enrollment = _get_enrollment_for_user(request.user, course)
    submission = Submission.objects.create(enrollment=enrollment)
    questions = course.questions.prefetch_related("choices").all()

    for question in questions:
        raw_choice_ids = request.POST.getlist(f"choice_{question.id}")
        valid_choices = Choice.objects.filter(question=question, id__in=raw_choice_ids)
        submission.choices.add(*valid_choices)

    messages.success(request, "Your assessment has been submitted.")
    return redirect(
        "onlinecourse:show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission.objects.select_related("enrollment__learner__user", "enrollment__course").prefetch_related("choices"),
        pk=submission_id,
        enrollment__course=course,
        enrollment__learner__user=request.user,
    )

    questions = course.questions.prefetch_related("choices").all()
    selected_ids = list(submission.choices.values_list("id", flat=True))
    question_results = []
    total_score = 0
    possible_score = 0

    for question in questions:
        question_grade = max(question.grade, 0)
        is_correct = question.is_get_score(selected_ids)
        possible_score += question_grade
        if is_correct:
            total_score += question_grade
        question_results.append(
            {
                "question": question,
                "is_correct": is_correct,
                "selected_choices": question.choices.filter(id__in=selected_ids),
                "correct_choices": question.choices.filter(is_correct=True),
            }
        )

    grade = round((total_score / possible_score) * 100) if possible_score else 0
    context = {
        "course": course,
        "submission": submission,
        "question_results": question_results,
        "total_score": total_score,
        "possible_score": possible_score,
        "grade": grade,
        "passed": grade >= 50,
    }
    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
