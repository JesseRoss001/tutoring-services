from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Product, Course, Session, Review, LiveStream, Student, AvailableHour, GroupSession, CourseSession, Payment, Enrollment


# Helper function to handle repeated registrations
def register_admin(model, admin_class):
    try:
        admin.site.register(model, admin_class)
    except AlreadyRegistered:
        pass

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title',)
    list_filter = ('price',)

class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_time', 'end_time', 'max_participants')
    search_fields = ('course__title',)
    list_filter = ('course', 'start_time', 'end_time')
    ordering = ('-start_time',)

class GroupSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'max_participants', 'cost')
    search_fields = ('title',)
    list_filter = ('start_time', 'end_time')
    ordering = ('-start_time',)

class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'specific_date', 'start_time', 'end_time', 'is_available', 'is_recurring')
    list_filter = ('day_of_week', 'is_available', 'is_recurring')
    search_fields = ('day_of_week', 'specific_date')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'get_participants')
    search_fields = ('title', )
    list_filter = ('start_time', 'end_time')
    ordering = ('start_time',)  # Ensures ordering by the 'start_time'

    def get_participants(self, obj):
        return ", ".join([student.name for student in obj.participants.all()])
    get_participants.short_description = 'Participants'

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
    
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_date')
    search_fields = ('student__name', 'course__title')
    list_filter = ('enrolled_date', 'course')

# Register all models using the helper function to handle any AlreadyRegistered errors
register_admin(Course, CourseAdmin)
register_admin(Student, StudentAdmin)
register_admin(CourseSession, CourseSessionAdmin)
register_admin(GroupSession, GroupSessionAdmin)
register_admin(Session, SessionAdmin)
register_admin(Review, ReviewAdmin)
register_admin(Product, ProductAdmin)
register_admin(LiveStream, LiveStreamAdmin)
register_admin(Payment, PaymentAdmin)
register_admin(AvailableHour, AvailableHourAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)