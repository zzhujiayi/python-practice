from rest_framework import serializers
from .models import Spring, Task
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()


class SpringSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Spring
        fields = ('id', 'name', 'description', 'end', 'links')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('spring-detail', kwargs={'pk': obj.pk}, request=request),
            'tasks': reverse('task-list', request=request) + '?spring={}'.format(obj.pk),
        }


class TaskSerializer(serializers.ModelSerializer):
    assigned = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD, required=False, allow_null=True, queryset=User.objects.all())
    status_display = serializers.SerializerMethodField()

    links = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'spring', 'status_display',
                  'order', 'assigned', 'started', 'due', 'completed', 'links')

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': reverse('task-detail', kwargs={'pk': obj.pk}, request=request),
            'spring': None,
            'assigned': None
        }

        if obj.spring_id:
            links['spring'] = reverse(
                'spring-detail', kwargs={'pk': obj.spring_id}, request=None)

        if obj.assigned:
            links['assigned'] = reverse(
                'user-detail', kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)

        return links


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        return {
            'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: obj.pk}, request=request),
            'tasks': '{}?assigned={}'.format(reverse('task-list', request=request), username)
        }
