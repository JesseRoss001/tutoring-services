from django.contrib import admin
from .models import Course, Student, Session, Review, StoreItem

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Session)
admin.site.register(Review)
admin.site.register(StoreItem)
