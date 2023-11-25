# myapp/serializers.py
from rest_framework import serializers
from user import models as userviewmodels

#Serializer is used to convert complex data types, such as Django models, 
# into Python data types that can be easily converted to JSON and vice versa.

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = userviewmodels.WishListItem
        fields = '__all__'