from datetime import date, datetime
import json

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers

from .models import Lesson, Student, Invoice, Group


def get_total_hours(user):
    return sum([lesson.duration_in_hours for lesson in user.profile.lesson_set.all()])


def get_total_earned(user):
    return sum([lesson.duration_in_hours * lesson.student.rate_per_hour for lesson in user.profile.lesson_set.all()])


def get_monthly_earnings(user):
    return sum([lesson.duration_in_hours * lesson.student.rate_per_hour for lesson in user.profile.lesson_set.all() if (lesson.date.month == datetime.now().month) and (lesson.date.year == datetime.now().year)])


def get_all_previous_monthly_earnings(user):
    previous_monthly_earnings = {}

    for month in range(1, 13):
        earnings = sum([lesson.duration_in_hours * lesson.student.rate_per_hour for lesson in user.profile.lesson_set.all() if (lesson.date.month == month) and (lesson.date.year == datetime.now().year - 1)])
        previous_monthly_earnings[month] = earnings
    return previous_monthly_earnings


def get_all_current_monthly_earnings(user):
    current_monthly_earnings = {}

    for month in range(1, 13):
        earnings = sum([lesson.duration_in_hours * lesson.student.rate_per_hour for lesson in user.profile.lesson_set.all() if (lesson.date.month == month) and (lesson.date.year == datetime.now().year)])
        current_monthly_earnings[month] = earnings
    return current_monthly_earnings


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'general/index.html'
    context_object_name = "context"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context.update({'hours_taught': get_total_hours(user)})
        context.update({'total_earned': get_total_earned(user)})
        context.update({'monthly_earnings': get_monthly_earnings(user)})
        print(self.request.user)
        print(user.profile.lesson_set.all())

        return context


class LessonCreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "lessons/lesson_create.html"

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        lesson = Lesson()
        lesson.student = Student.objects.get(pk=data["student"])
        lesson.date = data["date"]
        lesson.duration_in_hours = data["duration"]
        lesson.topic = data["topic"]
        lesson.report = data["report"]
        lesson.profile = request.user.profile
        lesson.save()

        # return self.get(self, request, *args, **kwargs)
        return redirect('lessons:view_lessons')


class LessonListView(LoginRequiredMixin, generic.ListView):
    model = Lesson
    template_name = "lessons/lesson_list.html"
    context_object_name = 'lessons'

    def get_queryset(self):
        return self.request.user.profile.lesson_set.all()


class LessonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = "lessons/lesson_detail.html"


class InvoiceCreateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "invoices/invoice_create.html"

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        print(data)

        students = Group.objects.get(pk=data["group"]).students.all()
        lessons = []
        for student in students:
            for lesson in student.lesson_set.all():
                if not lesson.is_invoiced:
                    lesson.is_invoiced = True
                    lesson.save()
                    lessons.append(lesson)

        invoice = Invoice()
        invoice.date = date.today()
        invoice.profile = request.user.profile
        invoice.group = Group.objects.get(pk=data["group"])
        invoice.save()
        invoice.lessons.set(lessons)
        invoice.save()

        return redirect('lessons:view_invoices')


class InvoiceListView(LoginRequiredMixin, generic.ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'

    def get_queryset(self):
        return self.request.user.profile.invoice_set.all()


class InvoiceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Invoice
    template_name = "invoices/invoice_detail.html"


class InvoiceDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Invoice
    success_url = ""


def pay_invoice(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    invoice.is_paid = True
    invoice.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def export_as_json(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    lessons = invoice.lessons.all()
    json_serializer = serializers.json.Serializer()
    json_serialized = json_serializer.serialize(lessons)

    response = HttpResponse(json_serialized, content_type='application/json charset=utf-8')

    # add filename to response
    response['Content-Disposition'] = 'attachment; filename="lessons.json"'
    return response


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = Group
    template_name = "groups/group_list.html"
    context_object_name = 'groups'
    queryset = Group.objects.all()


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = 'students'
    queryset = Student.objects.all()


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "general/profile.html"
    context_object_name = "context"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'hours_taught': get_total_hours(self.request.user)})
        context.update({'total_earned': get_total_earned(self.request.user)})
        context.update({'previous_monthly_earnings_json': json.dumps(get_all_previous_monthly_earnings(self.request.user))})
        context.update({'current_monthly_earnings_json': json.dumps(get_all_current_monthly_earnings(self.request.user))})

        return context


class AboutView(LoginRequiredMixin, generic.TemplateView):
    template_name = "general/about.html"


class HelpView(LoginRequiredMixin, generic.TemplateView):
    template_name = "general/help.html"
