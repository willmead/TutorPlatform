from django.contrib import admin
from .models import Subject, Student, Profile, Lesson, Invoice, Group


# Register your models here.
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(Invoice)
admin.site.register(Group)
# admin.site.register(Profile)


class StudentsInline(admin.TabularInline):
    model = Student
    classes = ['collapse']


class GroupsInline(admin.TabularInline):
    model = Group
    classes = ['collapse']


class InvoicesInline(admin.TabularInline):
    model = Invoice
    classes = ['collapse']


class LessonsInline(admin.TabularInline):
    model = Lesson
    classes = ['collapse']


class ProfileAdmin(admin.ModelAdmin):
    inlines = [
        StudentsInline,
        GroupsInline,
        LessonsInline,
        InvoicesInline,
    ]


admin.site.register(Profile, ProfileAdmin)
