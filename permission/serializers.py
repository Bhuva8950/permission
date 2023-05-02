from rest_framework import serializers
from permission.models import MyUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_allow = serializers.BooleanField(write_only=True)
    class Meta:
        model = MyUser
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "password",
            "is_allow",
        )
