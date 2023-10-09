from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import (
    User,
)


class UserSerializer(serializers.ModelSerializer):
    sections = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'sections',
                  'description',
                  'father_name',
                  'biography',
                  'website',
                  'linkedin',
                  'telegram',
                  'has_safe_pass',
                  'entering_year',
                  'field',
                  ]
        read_only_fields = ['username', 'id', 'has_safe_pass']


class UserPasswordUpdateSerializer(serializers.Serializer):
    new_pass = serializers.CharField(max_length=90, required=True, write_only=True)
    repeat = serializers.CharField(max_length=90, required=True, write_only=True)
    username = serializers.CharField(max_length=20, required=True, write_only=True)

    class Meta:
        fields = ['new_pass', 'repeat', 'username']

    def update(self, instance: User, validated_data):
        if validated_data['new_pass'] != validated_data['repeat']:
            raise serializers.ValidationError({'repeat': 'not correct'})
        instance.password = make_password(validated_data.pop('new_pass'))
        instance.has_safe_pass = True
        instance.save()
        return instance
