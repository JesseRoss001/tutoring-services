from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'app3_course'  # Unique table name for isolation

    def __str__(self):
        return self.title

class CourseSession(models.Model):
    course = models.ForeignKey(Course, related_name='sessions', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    meeting_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'app3_coursesession'

    def __str__(self):
        return f"{self.course.title} Session on {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    enrolled_courses = models.ManyToManyField(Course, through='Enrollment', related_name='students')
    booked_hours = models.ManyToManyField('AvailableHour', blank=True, related_name='students')
    purchased_products = models.ManyToManyField('Product', through='ProductPurchase', related_name='students')

    class Meta:
        db_table = 'app3_student'

    def __str__(self):
        return self.user.username if self.user else 'Unnamed Student'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'app3_enrollment'

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.title} on {self.enrolled_date}"

class Session(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    participants = models.ManyToManyField(Student)

    class Meta:
        db_table = 'app3_session'

    def __str__(self):
        return f"{self.title} from {self.start_time} to {self.end_time}"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app3_payment'

    def __str__(self):
        return f"Payment of {self.amount} by {self.student.name} for {self.course.title}"

class LiveStream(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default='No description provided')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    link = models.URLField()

    class Meta:
        db_table = 'app3_livestream'

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

    class Meta:
        db_table = 'app3_groupsession'

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @staticmethod
    def upcoming_group_sessions():
        now = timezone.now()
        return GroupSession.objects.filter(start_time__gte=now).order_by('start_time')

class AvailableHour(models.Model):
    specific_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(editable=False, null=True)
    is_available = models.BooleanField(default=True)
    is_recurring = models.BooleanField(null=True, default=False)

    class Meta:
        db_table = 'app3_availablehour'

    def save(self, *args, **kwargs):
        start_datetime = timezone.datetime.combine(self.specific_date, self.start_time)
        end_datetime = start_datetime + timezone.timedelta(hours=1)
        self.end_time = end_datetime.time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.specific_date}: {self.start_time} - {self.end_time}"

    @staticmethod
    def get_available_hours(date):
        return AvailableHour.objects.filter(specific_date=date, is_available=True)

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'app3_review'

    def __str__(self):
        return f"{self.course.title} - {self.rating}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    class Meta:
        db_table = 'app3_product'

    def __str__(self):
        return self.name

class ProductPurchase(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app3_productpurchase'

    def __str__(self):
        return f"{self.student.name} purchased {self.quantity} of {this.product.name}"
