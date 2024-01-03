from django.contrib import admin
from .models import Home
from .models import Task
from .models import Session
from .models import Planner
from .models import CalendarRow, CalendarDay

admin.site.register(Home)
admin.site.register(Task)
admin.site.register(Session)
admin.site.register(Planner)
class CalendarDayInline(admin.TabularInline):
    model = CalendarDay
class CalendarRowAdmin(admin.ModelAdmin):
    inlines = [CalendarDayInline]
admin.site.register(CalendarRow, CalendarRowAdmin)