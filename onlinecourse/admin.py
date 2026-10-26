import datetime

from django.contrib import admin
from django.utils import timezone

from .models import (
    Choice,
    Course,
    Enrollment,
    Instructor,
    Learner,
    Lesson,
    Question,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "course", "grade"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

    @admin.display(boolean=True, description="Published recently?")
    def was_published_recently(self, obj):
        return timezone.now() - datetime.timedelta(days=1) <= obj.pub_date <= timezone.now()


class LessonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title", "course", "content"]}),
        ("Date information", {"fields": ["created_at"]}),
    ]
    readonly_fields = ["created_at"]
    list_display = ("title", "course", "created_at")
    search_fields = ["title", "content", "course__name"]


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [(None, {"fields": ["name", "description"]})]
    list_display = ("name", "created_at")
    list_filter = ["created_at"]
    search_fields = ["name", "description"]
    inlines = [LessonInline, QuestionInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Lesson, LessonAdmin)
