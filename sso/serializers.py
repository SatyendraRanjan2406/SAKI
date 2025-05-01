from rest_framework import serializers
from user.models import User, UserProfile, UserAddress

class SSOUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'date_of_birth')

class SSOUserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ('street', 'city', 'pincode')

class SSOUserSerializer(serializers.ModelSerializer):
    profile = SSOUserProfileSerializer(source='userprofile')
    address = SSOUserAddressSerializer(source='useraddress', required=False)

    class Meta:
        model = User
        fields = ('email', 'date_joined', 'profile', 'address') 