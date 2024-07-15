from django.contrib import admin
from .models import Course, Student, CourseSession, GroupSession, Session, Review, Product, LiveStream, Payment, AvailableHour

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title',)
    list_filter = ('price',)

class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_time', 'end_time', 'max_participants', 'cost')
    search_fields = ('course__title',)
    list_filter = ('course', 'start_time', 'end_time')
    ordering = ('-start_time',)
    fields = ('course', 'start_time', 'end_time', 'max_participants', 'cost')

class GroupSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'max_participants', 'cost')
    search_fields = ('title',)
    list_filter = ('start_time', 'end_time')
    ordering = ('-start_time',)
    fields = ('title', 'description', 'start_time', 'end_time', 'max_participants', 'cost')

class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'specific_date', 'start_time', 'end_time', 'is_available', 'is_recurring')
    list_filter = ('day_of_week', 'is_available', 'is_recurring')
    search_fields = ('day_of_week', 'specific_date')



class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'duration', 'event_type', 'available_slots')
    search_fields = ('student__name', 'event_type')
    list_filter = ('event_type', 'date')
    ordering = ('-date',)
    fields = ('student', 'date', 'duration', 'event_type', 'description', 'available_slots')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'rating', 'created_at')
    search_fields = ('course__title', 'student__name')
    list_filter = ('rating', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_filter = ('price',)

class LiveStreamAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')
    search_fields = ('title',)
    list_filter = ('start_time', 'end_time')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('session', 'status', 'total')
    search_fields = ('session__student__name',)
    list_filter = ('status', 'created')

admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(CourseSession, CourseSessionAdmin)
admin.site.register(GroupSession, GroupSessionAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(LiveStream, LiveStreamAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(AvailableHour, AvailableHourAdmin)
