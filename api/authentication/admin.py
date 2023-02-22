#############
# LIBRARIES #
#############
from django.contrib import admin
from .models import User


#####################
# Registered models #
#####################
admin.site.register(User)
