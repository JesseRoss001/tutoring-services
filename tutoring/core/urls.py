from django.conf import settings
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/sessions/', views.course_session_list, name='course_session_list'),
    path('courses/sessions/<int:course_session_id>/', views.course_session_detail, name='course_session_detail'),
    path('courses/sessions/join/<int:course_session_id>/', views.join_course_session, name='join_course_session'),
    path('group-sessions/', views.group_session_list, name='group_session_list'),
    path('group-sessions/<int:group_session_id>/', views.group_session_detail, name='group_session_detail'),
    path('group-sessions/join/<int:group_session_id>/', views.join_group_session, name='join_group_session'),
    path('live-streams/', views.live_stream_list, name='live_stream_list'),
    path('live-streams/<int:live_stream_id>/', views.live_stream_detail, name='live_stream_detail'),
    path('available-hours/', views.available_hours_list, name='available_hours_list'),
    path('available-hours/<str:date>/', views.available_hour_detail, name='available_hour_detail'),
    path('book-available-hour/<int:hour_id>/', views.book_available_hour, name='book_available_hour'),
    path('reviews/', views.reviews, name='reviews'),
    path('api/reviews/', views.reviews_api, name='reviews_api'),
    path('store/', views.store, name='store'),
    path('api/store-items/', views.store_items_api, name='store_items_api'),
    path('create-checkout-session/', views.create_stripe_checkout_session, name='create-checkout-session'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),
    path('schedule/', include('schedule.urls')),
    path('payments/', include('payments.urls')),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('create-stripe-checkout-session-for-hour/', views.create_stripe_checkout_session_for_hour,name='create_stripe_checkout_session_for_hour'),
    path('payment-success-hour/', views.payment_success_hour, name='payment_success_hour'),
    path('payment-cancel-hour/', views.payment_cancel_hour, name='payment_cancel_hour'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
