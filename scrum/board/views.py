from rest_framework import viewsets, authentication, permissions, filters
from .models import Spring, Task
from .serializers import SpringSerializer, TaskSerializer, UserSerializer
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()


class DefaultsMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication
    )

    permission_classes = (
        permissions.IsAuthenticated,
    )

    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )


class SpringViewSet(viewsets.ModelViewSet):
    queryset = Spring.objects.order_by('end')
    serializer_class = SpringSerializer


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewset(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD

    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
