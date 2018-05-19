from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer, IncidentSerializer
from .models import Incident


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Incident.objects.all().order_by('-datetime')
    serializer_class = IncidentSerializer
