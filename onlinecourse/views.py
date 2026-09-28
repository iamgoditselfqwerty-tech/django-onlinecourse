from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = []
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            selected_choices.append(int(value))

    submission.choices.set(Choice.objects.filter(id__in=selected_choices))
    submission_id = submission.id

    return HttpResponseRedirect(
        reverse('onlinecourse:exam_result', args=(course_id, submission_id))
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, id=submission_id)
    choices = submission.choices.all()

    total_score = 0
    for choice in choices:
        if choice.is_correct:
            total_score += choice.question.grade

    context = {
        'course': course,
        'grade': total_score,
        'choices': choices,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)