from django.shortcuts import render, get_object_or_404
from .models import Course, Session, Review

def home(request):
    return render(request, 'core/home.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'core/course_detail.html', {'course': course})

def book_session(request):
    # Implementation of booking form and logic goes here
    pass

def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'core/reviews.html', {'reviews': reviews})
