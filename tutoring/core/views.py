# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Product, Course, Session, Review, LiveStream, RecordedCourse, Student, AvailableHour
from .serializers import ProductSerializer
from django.core.paginator import Paginator  # Correct import
import json
from django.utils import timezone
from datetime import datetime, timedelta
from schedule.models import Calendar, Event, Occurrence  # Import from Django-Scheduler
from payments import get_payment_model, RedirectNeeded
from django.db import models  # Add this import

Payment = get_payment_model()

def home(request):
    return render(request, 'core/home.html')

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'core/course_detail.html', {'course': course})
def book_session(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student_id = request.POST.get('student_id')
        available_hour_id = request.POST.get('available_hour_id')
        
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(Student, id=student_id) if student_id else None
        available_hour = get_object_or_404(AvailableHour, id=available_hour_id)

        calendar, _ = Calendar.objects.get_or_create(name='Sessions')

        start_datetime = datetime.combine(
            available_hour.specific_date or datetime.today(), available_hour.start_time)
        end_datetime = datetime.combine(
            available_hour.specific_date or datetime.today(), available_hour.end_time)

        event = Event.objects.create(
            title=f"Session for {course.title}",
            start=start_datetime,
            end=end_datetime,
            calendar=calendar
        )

        Occurrence.objects.create(
            event=event,
            start=start_datetime,
            end=end_datetime
        )

        session = Session.objects.create(
            course=course,
            student=student,
            date=start_datetime,
            duration=end_datetime - start_datetime,
            event_type='1-to-1' if student else 'group'
        )

        if course.price > 0:
            payment = Payment.objects.create(
                variant='default',
                description=f"Payment for {session.course.title}",
                total=course.price,
                session=session,
                user=request.user
            )
            try:
                payment.save()
                return redirect(payment.get_process_url())
            except RedirectNeeded as redirect_to:
                return redirect(str(redirect_to))
        else:
            return redirect('course_detail', course_id=course_id)

    courses = Course.objects.all()
    students = Student.objects.all()
    available_hours = AvailableHour.objects.all()
    today = timezone.now()
    next_30_days = [today + timedelta(days=i) for i in range(30)]
    events = Event.objects.filter(start__range=(today, today + timedelta(days=30)))

    events_data = []
    for event in events:
        total_slots = event.calendar.event_set.aggregate(total=models.Count('occurrence'))['total']
        filled_slots = event.occurrence_set.count()
        events_data.append({
            'event': event,
            'total_slots': total_slots,
            'filled_slots': filled_slots
        })

    return render(request, 'core/book_session.html', {
        'courses': courses,
        'students': students,
        'available_hours': available_hours,
        'next_30_days': next_30_days,
        'events_data': events_data
    })
# views.py
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    occurrences = event.occurrence_set.all()
    return render(request, 'core/event_detail.html', {'event': event, 'occurrences': occurrences})

def reviews(request):
    reviews = Review.objects.all().values('id', 'course__title', 'review_text', 'rating', 'created_at')
    reviews_json = json.dumps(list(reviews), default=str)
    return render(request, 'core/reviews.html', {'reviews_json': reviews_json, 'reviews': reviews})

def reviews_api(request):
    try:
        reviews = Review.objects.all().values('id', 'course__title', 'review_text', 'rating', 'created_at')
        return JsonResponse(list(reviews), safe=False)
    except Exception as e:
        logger.error(f"Failed to fetch reviews: {str(e)}")  # Ensure you have logging configured
        return JsonResponse({'error': str(e)}, status=500)
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def store(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/store.html', {'page_obj': page_obj, 'query': query})

def store_items_api(request):
    try:
        items = Product.objects.all().values('id', 'name', 'description', 'price', 'image')
        return JsonResponse(list(items), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
