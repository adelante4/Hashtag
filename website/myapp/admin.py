from django.contrib import admin

# Register your models here.
from myapp.models import *
admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Cinema)
admin.site.register(Showtimes)
admin.site.register(Ticket)