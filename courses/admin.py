from django.contrib import admin
from .models import course, RatingReview,TypeAR,TypeEN,Price,CoursePrevEN,CoursePrevAR


# Register your models here.
class courseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('course_name',)}
    list_display = ( 'course_name','img')
admin.site.register(course,courseAdmin)
admin.site.register(RatingReview)
admin.site.register(TypeEN)
admin.site.register(TypeAR)
admin.site.register(Price)
admin.site.register(CoursePrevEN)
admin.site.register(CoursePrevAR)

