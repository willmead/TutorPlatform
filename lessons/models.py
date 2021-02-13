from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    subjects = models.ManyToManyField(Subject)
    notes = models.TextField()
    rate_per_hour = models.IntegerField(default=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=256)
    students = models.ManyToManyField(Student)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateTimeField()
    duration_in_hours = models.FloatField()
    topic = models.CharField(max_length=256, default="General")
    report = models.TextField()
    is_invoiced = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def total(self):
        return self.student.rate_per_hour * self.duration_in_hours

    def __str__(self):
        return f"{self.student} ({self.date})"


class Invoice(models.Model):
    lessons = models.ManyToManyField(Lesson)
    date = models.DateField()
    is_paid = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

    def total(self):
        return sum([lesson.total() for lesson in self.lessons.all()])

    def __str__(self):
        return f"{self.date}"


@receiver(pre_delete, sender=Invoice, dispatch_uid='invoice_delete_signal')
def uninvoice_lessons(sender, instance, using, **kwargs):
    for lesson in instance.lessons.all():
        lesson.is_invoiced = False
        lesson.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
