from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(theClient)
admin.site.register(theAdmin)
admin.site.register(ProjectRequest)
admin.site.register(Milestone)