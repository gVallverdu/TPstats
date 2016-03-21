from django.contrib import admin
from .models import Measure, Experiment, Glassware

# Register your models here.
admin.site.register(Measure)
admin.site.register(Experiment)
admin.site.register(Glassware)
