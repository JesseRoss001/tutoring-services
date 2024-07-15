from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from schedule.models import Calendar, Event, Occurrence  # Import from Django-Scheduler
from payments.models import BasePayment  # Import from Django-Payments


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

class CourseSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.course.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @staticmethod
    def upcoming_course_sessions():
        now = timezone.now()
        return CourseSession.objects.filter(start_time__gte=now).order_by('start_time')

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Session(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    duration = models.DurationField()
    event_type = models.CharField(max_length=20, choices=[
        ('1-to-1', '1-to-1'),
        ('group', 'Group'),
        ('live_stream', 'Live Stream'),
        ('testing', 'Testing')
    ])
    description = models.TextField(blank=True)
    available_slots = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.event_type} - {self.date.strftime('%Y-%m-%d %H:%M')}"

class Payment(BasePayment):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='No description provided')  # Adding a default value
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    link = models.URLField()

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @staticmethod
    def upcoming_live_streams():
        now = timezone.now()
        return LiveStream.objects.filter(start_time__gte=now).order_by('start_time')

class GroupSession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @staticmethod
    def upcoming_group_sessions():
        now = timezone.now()
        return GroupSession.objects.filter(start_time__gte=now).order_by('start_time')
class AvailableHour(models.Model):
    day_of_week = models.CharField(max_length=9, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], blank=True, null=True)
    specific_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=False)  # Not available by default
    is_recurring = models.BooleanField(default=False)  # New field to handle recurring hours

    def __str__(self):
        if self.specific_date:
            return f"{self.specific_date}: {self.start_time} - {self.end_time}"
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"

    @staticmethod
    def get_available_hours(date):
        day_of_week = date.strftime('%A')
        specific_hours = AvailableHour.objects.filter(specific_date=date, is_available=True)
        recurring_hours = AvailableHour.objects.filter(day_of_week=day_of_week, is_available=True, is_recurring=True)
        return specific_hours | recurring_hours

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.course.title} - {self.rating}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Payment(BasePayment):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
