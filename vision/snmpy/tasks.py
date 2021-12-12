from celery import shared_task
from .lib.easysnmp import get
from pysnmp import hlapi
from .models import Node


@shared_task
def pollNode(uid):
    node = Node.objects.get(uid=uid)
    hostname = get(node.ip, ['1.3.6.1.2.1.1.5.0'], hlapi.CommunityData(node.snmpCommunityString))
    description = get(node.ip, ['1.3.6.1.2.1.1.1.0'], hlapi.CommunityData(node.snmpCommunityString))
    if hostname:
        if node.name == '':
            node.name = hostname["1.3.6.1.2.1.1.5.0"]
        node.snmpHostname = hostname["1.3.6.1.2.1.1.5.0"]
        node.snmpDescription = description["1.3.6.1.2.1.1.1.0"]
        node.save()
