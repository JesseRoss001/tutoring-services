from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from schedule.models import Calendar, Event, Occurrence  # Import from Django-Scheduler
from payments.models import BasePayment  # Import from Django-Payments
from phonenumber_field.modelfields import PhoneNumberField

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

class CourseSession(models.Model):
    course = models.ForeignKey(Course, related_name='sessions', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    meeting_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.course.title} Session on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=False, null=True, blank=True)  # Removed unique constraint for migration
    phone = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else 'Unnamed Student'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.title} on {self.enrolled_date}"

class Session(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.ManyToManyField(Student)

    def __str__(self):
        return f"{self.title} from {self.start_time} to {self.end_time}"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.student.name} for {self.course.title}"


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
    meeting_url = models.URLField(blank=True, null=True)
    

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
