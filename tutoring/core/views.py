from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Product, Course, Session, Review, LiveStream, Student, AvailableHour, GroupSession, CourseSession, Payment, Enrollment
from .serializers import ProductSerializer
from django.core.paginator import Paginator
import json
import stripe
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from schedule.models import Calendar, Event, Occurrence
from payments import get_payment_model, RedirectNeeded
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

stripe.api_key = settings.STRIPE_SECRET_KEY


Payment = get_payment_model()




def home(request):
    return render(request, 'core/home.html')

def live_stream_list(request):
    try:
        live_streams = LiveStream.upcoming_live_streams()
        return render(request, 'core/live_stream_list.html', {'live_streams': live_streams})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def live_stream_detail(request, live_stream_id):
    try:
        live_stream = get_object_or_404(LiveStream, id=live_stream_id)
        return render(request, 'core/live_stream_detail.html', {'live_stream': live_stream})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def group_session_list(request):
    try:
        group_sessions = GroupSession.upcoming_group_sessions()
        return render(request, 'core/group_session_list.html', {'group_sessions': group_sessions})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def group_session_detail(request, group_session_id):
    try:
        group_session = get_object_or_404(GroupSession, id=group_session_id)
        return render(request, 'core/group_session_detail.html', {'group_session': group_session})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def join_group_session(request, group_session_id):
    try:
        group_session = get_object_or_404(GroupSession, id=group_session_id)
        if request.method == 'POST':
            if group_session.max_participants > group_session.participants.count():
                group_session.participants.add(request.user)
                return redirect('group_session_detail', group_session_id=group_session_id)
            else:
                return render(request, 'core/group_session_detail.html', {'group_session': group_session, 'error': 'No slots available'})
        return render(request, 'core/join_group_session.html', {'group_session': group_session})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def course_list(request):
    try:
        courses = Course.objects.all()
        return render(request, 'core/course_list.html', {'courses': courses})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})



def course_session_list(request):
    try:
        course_sessions = CourseSession.upcoming_course_sessions()
        return render(request, 'core/course_session_list.html', {'course_sessions': course_sessions})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def course_session_detail(request, course_session_id):
    try:
        course_session = get_object_or_404(CourseSession, id=course_session_id)
        return render(request, 'core/course_session_detail.html', {'course_session': course_session})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def join_course_session(request, course_session_id):
    try:
        course_session = get_object_or_404(CourseSession, id=course_session_id)
        if request.method == 'POST':
            if course_session.max_participants > course_session.participants.count():
                course_session.participants.add(request.user)
                return redirect('course_session_detail', course_session_id=course_session_id)
            else:
                return render(request, 'core/course_session_detail.html', {'course_session': course_session, 'error': 'No slots available'})
        return render(request, 'core/join_course_session.html', {'course_session': course_session})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def available_hours_list(request):
    try:
        today = timezone.now().date()
        next_30_days = [today + timedelta(days=i) for i in range(30)]
        days_status = {}
        for day in next_30_days:
            hours = AvailableHour.get_available_hours(day)
            days_status[day] = hours.exists()
        return render(request, 'core/available_hours_list.html', {'days_status': days_status})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def available_hour_detail(request, date):
    try:
        date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        available_hours = AvailableHour.get_available_hours(date_obj)
        return render(request, 'core/available_hour_detail.html', {'available_hours': available_hours, 'date': date_obj})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def book_available_hour(request, available_hour_id):
    try:
        available_hour = get_object_or_404(AvailableHour, id=available_hour_id)
        if request.method == 'POST':
            if available_hour.is_available:
                available_hour.is_available = False
                available_hour.save()
                session = Session.objects.create(
                    date=timezone.now().replace(
                        year=available_hour.specific_date.year if available_hour.specific_date else timezone.now().year,
                        month=available_hour.specific_date.month if available_hour.specific_date else timezone.now().month,
                        day=available_hour.specific_date.day if available_hour.specific_date else timezone.now().day,
                        hour=available_hour.start_time.hour,
                        minute=available_hour.start_time.minute,
                        second=0
                    ),
                    duration=timedelta(hours=1),
                    event_type='1-to-1',
                    available_slots=1
                )
                return redirect('available_hours_list')
            else:
                return render(request, 'core/available_hour_detail.html', {'available_hour': available_hour, 'error': 'This hour is no longer available'})
        return render(request, 'core/book_available_hour.html', {'available_hour': available_hour})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

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

def event_detail(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        return render(request, 'core/event_detail.html', {'event': event})
    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def course_detail(request, course_id):
    """Display course detail page with Stripe payment option."""
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'core/course_detail.html', {
        'course': course, 
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })

@csrf_exempt
@require_http_methods(["POST"])
def create_stripe_checkout_session(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User must be authenticated'}, status=403)

    try:
        body = json.loads(request.body)
        course_id = body.get('course_id')
        course = Course.objects.get(id=course_id)
        success_url = request.build_absolute_uri(reverse('payment_success')) + '?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = request.build_absolute_uri(reverse('payment_cancel'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {'name': course.title},
                    'unit_amount': int(course.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={'course_id': course_id, 'user_id': request.user.id}
        )
        return JsonResponse({'sessionId': session.id})
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def payment_success(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        metadata = session.metadata
        course_id = metadata['course_id']
        user_id = metadata['user_id']

        course = Course.objects.get(id=course_id)
        user = User.objects.get(id=user_id)
        student, created = Student.objects.get_or_create(user=user)

        Enrollment.objects.create(student=student, course=course)
        return render(request, 'core/payment_success.html', {'course': course})
    else:
        return HttpResponse('Payment failed or cancelled', status=400)
    
def payment_cancel(request):
    return render(request, 'core/payment_cancel.html')