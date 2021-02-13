from django.urls import path

from . import views

app_name = 'lessons'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # Lessons
    path('lessons/', views.LessonListView.as_view(), name='view_lessons'),
    path('lesson/add', views.LessonCreateView.as_view(), name='add_lesson'),
    path('lessons/<int:pk>', views.LessonDetailView.as_view(), name='view_lesson'),

    # Invoices
    path('invoices/', views.InvoiceListView.as_view(), name='view_invoices'),
    path('invoices/add', views.InvoiceCreateView.as_view(), name="add_invoice"),
    path('invoices/<int:pk>', views.InvoiceDetailView.as_view(), name="view_invoice"),
    path('invoices/delete/<int:pk>', views.InvoiceDeleteView.as_view(), name="delete_invoice"),
    path('invoices/pay/<int:pk>', views.pay_invoice, name="pay_invoice"),

    # Students
    path('students/', views.StudentListView.as_view(), name='view_students'),
    # path('students/add', view.StudentCreateView.as_view(), name='add_student'),
    # path('students/<int:pk>', views.StudentDetailView.as_view(), name='view_student'),

    # Groups
    path('groups/', views.GroupListView.as_view(), name='view_groups'),
    # path('groups/add', view.GroupCreateView.as_view(), name='add_group'),
    # path('groups/<int:pk>', views.GroupDetailView.as_view(), name='view_group'),

    # General
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('about/', views.AboutView.as_view(), name='about')

]
