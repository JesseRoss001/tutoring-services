# admin.py
from django.contrib import admin
from .models import Course, Student, Session, Review, Product, LiveStream, Payment, AvailableHour

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Review)
admin.site.register(Product)
admin.site.register(LiveStream)
admin.site.register(Payment)
admin.site.register(AvailableHour)
