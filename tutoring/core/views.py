from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .models import Course, Session, Review, Product
import json

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
    products = Product.objects.all()
    return render(request, 'core/store.html', {'products': products})

def store_items_api(request):
    try:
        items = Product.objects.all().values('id', 'name', 'description', 'price', 'image', 'subject', 'exam_board', 'age_range', 'created_at')
        return JsonResponse(list(items), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
