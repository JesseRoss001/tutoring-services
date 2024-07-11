from django.conf import settings
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('book/', views.book_session, name='book_session'),
    path('reviews/', views.reviews, name='reviews'),
    path('api/reviews/', views.reviews_api, name='reviews_api'),
    path('store/', views.store, name='store'),
    path('api/store-items/', views.store_items_api, name='store_items_api'),
    path('schedule/', include('schedule.urls')),  # Include the schedule URLs
    path('payments/', include('payments.urls')),  # Include the payment URLs
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include the router URLs
urlpatterns += router.urls