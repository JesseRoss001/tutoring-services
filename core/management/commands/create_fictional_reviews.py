from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Course, Student, Review

class Command(BaseCommand):
    help = 'Create fictional reviews for testing'

    def handle(self, *args, **kwargs):
        try:
            with transaction.atomic():
                # Create some courses
                course1 = Course.objects.create(title='Mathematics GCSE', description='Mathematics course for GCSE students.', price=200.00)
                course2 = Course.objects.create(title='Mathematics A-Level', description='Mathematics course for A-Level students.', price=250.00)

                # Create some students
                student1 = Student.objects.create(name='John Doe', email='john.doe@example.com', phone='1234567890')
                student2 = Student.objects.create(name='Jane Smith', email='jane.smith@example.com', phone='0987654321')

                # Create some reviews
                Review.objects.create(course=course1, student=student1, review_text='Great course! Very helpful for my GCSEs.', rating=5)
                Review.objects.create(course=course1, student=student2, review_text='The tutor was amazing and explained everything clearly.', rating=4)
                Review.objects.create(course=course2, student=student1, review_text='Challenging but rewarding. Perfect for A-Level preparation.', rating=5)
                Review.objects.create(course=course2, student=student2, review_text='Excellent course. Helped me a lot with my exams.', rating=4)

                self.stdout.write(self.style.SUCCESS('Successfully created fictional reviews'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Error creating reviews: %s' % e))
