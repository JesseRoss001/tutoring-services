from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django import template
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
from decimal import Decimal
from schedule.models import Calendar, Event, Occurrence
from payments import get_payment_model, RedirectNeeded
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm
from django.utils.safestring import mark_safe

stripe.api_key = settings.STRIPE_SECRET_KEY


Payment = get_payment_model()



def home(request):
    user_courses = False  # Default to no courses
    if request.user.is_authenticated:
        # Only query enrollments if the user is logged in
        user_courses = Enrollment.objects.filter(student__user=request.user).exists()
    
    return render(request, 'core/home.html', {'user_courses': user_courses})
@login_required
def profile(request):
    try:
        student = get_object_or_404(Student, user=request.user)
    except Exception as e:
        print(f"Error fetching student for user {request.user}: {e}")
        return render(request, 'core/error.html', {'error': 'Student profile not found'})

    # Retrieve enrollments, booked hours, and purchased products
    enrollments = student.enrolled_courses.all()
    booked_hours = student.booked_hours.all().order_by('specific_date', 'start_time')  # Order the booked hours
    purchased_products = student.purchased_products.all()

    context = {
        'student': student,
        'enrollments': enrollments,
        'booked_hours': booked_hours,
        'purchased_products': purchased_products,
    }

    return render(request, 'core/profile.html', context)


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

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and get the instance
            user = form.save()

            # Create a Student instance with the name from the form
            student = Student.objects.create(
                user=user,
                name=form.cleaned_data.get('name'),  # Ensure name is saved
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get('phone')
            )

            # Log in the user
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'core/signup.html', {'form': form})



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




@login_required
def course_session_list(request):
    user = request.user
    if hasattr(user, 'student'):
        student = user.student
        enrolled_courses_ids = list(Enrollment.objects.filter(student=student).values_list('course_id', flat=True))

        # Debugging: Detailed information
        print(f"User: {user.username}, Student ID: {student.id}")
        print(f"Enrolled Course IDs: {enrolled_courses_ids}")

        # Query course sessions for enrolled courses
        course_sessions = CourseSession.objects.filter(course_id__in=enrolled_courses_ids)

        # Debug: Print each session's details
        for session in course_sessions:
            print(f"Session: {session.course.title} on {session.start_time}, Course ID: {session.course.id}")

        context = {'course_sessions': course_sessions}
        return render(request, 'core/course_session_list.html', context)
    else:
        print("User is not a student")
        return render(request, 'core/course_session_list.html', {'course_sessions': []})




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

        return render(request, 'core/available_hour_detail.html', {
            'available_hours': available_hours,
            'date': date_obj,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })

    except Exception as e:
        return render(request, 'core/error.html', {'error': str(e)})

def book_available_hour(request, available_hour_id):
    try:
        available_hour = get_object_or_404(AvailableHour, id=available_hour_id)

        if request.method == 'POST':
            if available_hour.is_available:
                # Mark the hour as no longer available
                available_hour.is_available = False
                available_hour.save()

                # Get the student associated with the current user
                student = Student.objects.get(user=request.user)

                # Add the available hour to the student's booked hours
                student.booked_hours.add(available_hour)

                # Create a session for the booked hour
                session = Session.objects.create(
                    title='1-to-1 Session',
                    start_time=timezone.datetime.combine(available_hour.specific_date, available_hour.start_time),
                    end_time=timezone.datetime.combine(available_hour.specific_date, available_hour.end_time)
                )
                session.participants.add(student)

                return redirect('available_hours_list')
            else:
                return render(request, 'core/available_hour_detail.html', {
                    'available_hour': available_hour,
                    'error': 'This hour is no longer available'
                })

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

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_stripe_checkout_session_for_hour(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User must be authenticated'}, status=403)

    try:
        body = json.loads(request.body)
        hour_id = body.get('hour_id')
        available_hour = AvailableHour.objects.get(id=hour_id)
        success_url = request.build_absolute_uri(reverse('payment_success_hour')) + '?session_id={CHECKOUT_SESSION_ID}'
        cancel_url = request.build_absolute_uri(reverse('payment_cancel_hour'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'gbp',
                    'product_data': {'name': '1-to-1 Session'},
                    'unit_amount': 1500,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={'hour_id': hour_id, 'user_id': request.user.id}
        )
        return JsonResponse({'sessionId': session.id})
    except AvailableHour.DoesNotExist:
        return JsonResponse({'error': 'Available hour not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def payment_success_hour(request):
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        metadata = session.metadata
        hour_id = metadata['hour_id']
        user_id = metadata['user_id']

        available_hour = AvailableHour.objects.get(id=hour_id)
        user = User.objects.get(id=user_id)
        student, created = Student.objects.get_or_create(user=user)

        # Mark the specific hour as booked
        available_hour.is_available = False
        available_hour.save()

        # Debugging: Check student before adding booked hour
        print(f"Before adding: Booked hours for {student.name}: {[str(hour) for hour in student.booked_hours.all()]}")

        # Add booked hour to student
        student.booked_hours.add(available_hour)

        # Debugging: Confirm addition
        print(f"After adding: Booked hours for {student.name}: {[str(hour) for hour in student.booked_hours.all()]}")

        # Create a session for the booked hour
        booked_session = Session.objects.create(
            title='1-to-1 Session',
            start_time=timezone.now().replace(
                year=available_hour.specific_date.year if available_hour.specific_date else timezone.now().year,
                month=available_hour.specific_date.month if available_hour.specific_date else timezone.now().month,
                day=available_hour.specific_date.day if available_hour.specific_date else timezone.now().day,
                hour=available_hour.start_time.hour,
                minute=available_hour.start_time.minute,
                second=0
            ),
            end_time=timezone.now().replace(
                year=available_hour.specific_date.year if available_hour.specific_date else timezone.now().year,
                month=available_hour.specific_date.month if available_hour.specific_date else timezone.now().month,
                day=available_hour.specific_date.day if available_hour.specific_date else timezone.now().day,
                hour=available_hour.end_time.hour,
                minute=available_hour.end_time.minute,
                second=0
            )
        )
        booked_session.participants.add(student)

        return render(request, 'core/payment_success_hour.html', {'session': booked_session})
    else:
        return HttpResponse('Payment failed or cancelled', status=400)


def payment_cancel_hour(request):
    return render(request, 'core/payment_cancel_hour.html')


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the cart, stored in session.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    # Add product to the cart or update its quantity
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1, 'price': str(product.price)}

    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    """
    Display the cart contents.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal(0)

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_item_price = Decimal(item['price']) * item['quantity']
        total_price += total_item_price
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'total_item_price': total_item_price,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'core/cart_detail.html', context)

@login_required
def remove_from_cart(request, product_id):
    """
    Remove an item from the cart.
    """
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart

    return redirect('cart_detail')

@login_required
def update_cart_item(request, product_id):
    """
    Update the quantity of an item in the cart.
    """
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))

    if str(product_id) in cart:
        if quantity > 0:
            cart[str(product_id)]['quantity'] = quantity
        else:
            del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_detail')

@login_required
def checkout(request):
    """
    Proceed to checkout page.
    """
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    # Clear the cart after checkout
    request.session['cart'] = {}
    return render(request, 'core/checkout.html')