#############
# LIBRARIES #
#############
from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


#####################
# Registered models #
####################
admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
