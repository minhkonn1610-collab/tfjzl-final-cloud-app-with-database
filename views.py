from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    Course,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission,
)


def is_get_score(submissions, total_questions):
    total_score = sum(
        1 for submission in submissions
        if submission.selected_choice.is_correct
    )
    possible_score = total_questions

    grade = (
        int((total_score / possible_score) * 100)
        if possible_score > 0
        else 0
    )

    return total_score, possible_score, grade


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    return render(
        request,
        'onlinecourse/course_details_bootstrap.html',
        {'course': course},
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
        'onlinecourse/exam.html',
        {
            'course': course,
            'questions': questions,
            'enrollment': enrollment,
        },
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.all()

    learner = get_object_or_404(
        Learner,
        user=request.user,
    )

    enrollment = get_object_or_404(
        Enrollment,
        learner=learner,
        course=course,
    )

    total = questions.count()

    for question in questions:
        choice_key = request.POST.get(
            f'choice_{question.id}'
        )

        if not choice_key:
            continue

        try:
            selected = Choice.objects.get(
                pk=choice_key,
                question=question,
            )

            Submission.objects.update_or_create(
                enrollment=enrollment,
                question=question,
                defaults={
                    'selected_choice': selected,
                },
            )

        except Choice.DoesNotExist:
            continue

    submissions = list(
        Submission.objects.filter(
            enrollment=enrollment,
            question__course=course,
        ).select_related(
            'question',
            'selected_choice',
        )
    )

    total_score, possible_score, grade = is_get_score(
        submissions,
        total,
    )

    correct = total_score
    passed = grade >= 50

    selected_ids = {
        submission.question_id: submission.selected_choice_id
        for submission in submissions
    }

    return render(
        request,
        'onlinecourse/exam_result.html',
        {
            'course': course,
            'grade': grade,
            'score': grade,
            'correct': correct,
            'total': total,
            'total_score': total_score,
            'possible_score': possible_score,
            'passed': passed,
            'submissions': submissions,
            'selected_ids': selected_ids,
        },
    )


@login_required
def show_exam_result(request, course_id):
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

    questions = course.questions.all()

    submissions = list(
        Submission.objects.filter(
            enrollment=enrollment,
            question__course=course,
        ).select_related(
            'question',
            'selected_choice',
        )
    )

    total = questions.count()

    total_score, possible_score, grade = is_get_score(
        submissions,
        total,
    )

    correct = total_score
    passed = grade >= 50

    selected_ids = {
        submission.question_id: submission.selected_choice_id
        for submission in submissions
    }

    return render(
        request,
        'onlinecourse/exam_result.html',
        {
            'course': course,
            'grade': grade,
            'score': grade,
            'correct': correct,
            'total': total,
            'total_score': total_score,
            'possible_score': possible_score,
            'passed': passed,
            'submissions': submissions,
            'selected_ids': selected_ids,
        },
    )
