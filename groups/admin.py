from django.contrib import admin
from . import models
# Register your models here.

class GroupMemberInLine(admin.TabularInline):
    model  = models.GroupMember
# 3:58 the above class is becasue our GroupMember has a parent model with group, by using a tabularinline class
# when we visit the admin page when we click on group we will be able to see the group members and edit those as well

admin.site.register(models.Group)
