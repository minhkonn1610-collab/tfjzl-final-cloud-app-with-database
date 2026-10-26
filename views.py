from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import (
    Course,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission,
)


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
    questions = course.questions.all()

    learner = get_object_or_404(
        Learner,
        user=request.user,
    )

    enrollment, _ = Enrollment.objects.get_or_create(
        learner=learner,
        course=course,
    )

    return render(
        request,
        "onlinecourse/exam.html",
        {
            "course": course,
            "questions": questions,
            "enrollment": enrollment,
        },
    )


@login_required
def submit(request, course_id):
    if request.method != "POST":
        return redirect("exam", course_id=course_id)

    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.all()

    learner = get_object_or_404(
        Learner,
        user=request.user,
    )

    enrollment, _ = Enrollment.objects.get_or_create(
        learner=learner,
        course=course,
    )

    # Create a submission for this attempt.
    submission = Submission.objects.create(
        enrollment=enrollment,
    )

    # Save the selected choices belonging to this course's questions.
    for question in questions:
        choice_id = request.POST.get(
            f"choice_{question.id}"
        )

        if not choice_id:
            continue

        choice = Choice.objects.filter(
            pk=choice_id,
            question=question,
        ).first()

        if choice is not None:
            submission.choices.add(choice)

    # Redirect to the result view after saving the answers.
    return redirect(
        "exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)

    learner = get_object_or_404(
        Learner,
        user=request.user,
    )

    enrollment = get_object_or_404(
        Enrollment,
        learner=learner,
        course=course,
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment=enrollment,
    )

    questions = course.questions.all()

    selected_ids = list(
        submission.choices.values_list("id", flat=True)
    )

    # Calculate earned points and possible points.
    grade = 0
    possible = 0
    correct = 0

    for question in questions:
        possible += question.grade

        if question.is_get_score(selected_ids):
            grade += question.grade
            correct += 1

    total = questions.count()

    # Percentage score for displaying the result.
    score = round(grade * 100 / possible) if possible > 0 else 0
    passed = score >= 50

    context = {
        "course": course,
        "submission": submission,
        "questions": questions,
        "selected_ids": selected_ids,
        "grade": grade,
        "possible": possible,
        "total_score": grade,
        "possible_score": possible,
        "score": score,
        "correct": correct,
        "total": total,
        "passed": passed,
    }

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        context,
    )
