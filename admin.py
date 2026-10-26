import datetime

from django.contrib import admin
from django.utils import timezone

from .models import (
    Course,
    Instructor,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission,
    Lesson,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

    inlines = [ChoiceInline]

    list_display = (
        'question_text',
        'pub_date',
        'was_published_recently',
    )

    list_filter = ['pub_date']
    search_fields = ['question_text']

    def was_published_recently(self, obj):
        return obj.pub_date >= (
            timezone.now() - datetime.timedelta(days=1)
        )

    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class LessonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Content', {'fields': ['content']}),
        ('Timestamps', {'fields': ['created_at']}),
    ]

    readonly_fields = ('created_at',)

    list_display = ('title', 'created_at')
    search_fields = ['title']


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Description', {'fields': ['description']}),
    ]

    list_display = ('name', 'created_at')
    search_fields = ['name']


admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Lesson, LessonAdmin)
