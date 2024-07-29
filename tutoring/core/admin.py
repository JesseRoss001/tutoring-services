from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Product, Course, Session, Review, LiveStream, Student, AvailableHour, GroupSession, CourseSession, Payment, Enrollment,DailySchedule


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
    list_display = ('title', 'start_time', 'end_time', 'max_participants')
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



class DailyScheduleAdmin(admin.ModelAdmin):
    change_list_template = 'admin/daily_schedule_change_list.html'
    list_display = ('get_today',)

    def get_today(self, obj):
        return timezone.now().date()
    get_today.short_description = 'Today'

    def changelist_view(self, request, extra_context=None):
        today = timezone.now().date()
        available_hours = AvailableHour.objects.filter(specific_date=today)
        group_sessions = GroupSession.objects.filter(start_time__date=today)
        course_sessions = CourseSession.objects.filter(start_time__date=today)
        live_streams = LiveStream.objects.filter(start_time__date=today)

        extra_context = extra_context or {}
        extra_context['available_hours'] = available_hours
        extra_context['group_sessions'] = group_sessions
        extra_context['course_sessions'] = course_sessions
        extra_context['live_streams'] = live_streams
        extra_context['today'] = today

        return super(DailyScheduleAdmin, self).changelist_view(request, extra_context=extra_context)
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
admin.site.register(DailySchedule, DailyScheduleAdmin)