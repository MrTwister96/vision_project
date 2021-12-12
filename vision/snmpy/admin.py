from django.contrib import admin
from .models import *

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'name', 'ip', 'snmpHostname']
    readonly_fields = ['snmpHostname', 'snmpDescription']
