from rest_framework import serializers
from .models import Notifications

#Convert python objects to json readable objects
class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'