from django.contrib import admin
from .models import Course, Student, Session, Review, Product  # Remove StoreItem

# Register your models here.
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Review)
admin.site.register(Product)  # Ensure Product is registered instead of StoreItem