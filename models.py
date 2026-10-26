from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="instructor",
    )
    full_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Learner(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="learner",
    )
    full_name = models.CharField(max_length=200)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Enrollment(models.Model):
    learner = models.ForeignKey(
        Learner,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("learner", "course")

    def __str__(self):
        return f"{self.learner.full_name} enrolled in {self.course.name}"


class Question(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="questions",
        null=True,
        blank=True,
    )
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        all_answers = self.choices.filter(
            is_correct=True
        ).count()

        selected_correct = self.choices.filter(
            is_correct=True,
            id__in=selected_ids,
        ).count()

        return all_answers > 0 and all_answers == selected_correct


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    choices = models.ManyToManyField(
        Choice,
        related_name="submissions",
    )

    def __str__(self):
        return (
            f"Submission {self.id} for enrollment {self.enrollment.id}"
        )


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
