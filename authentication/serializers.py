from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import (
    User,
    GolestanUser,
)
from django.contrib.auth.models import Group


class UserSerializer(serializers.ModelSerializer):
    teaching_sections = serializers.StringRelatedField(many=True, read_only=True)
    assistant_sections = serializers.StringRelatedField(many=True, read_only=True)
    student_sections = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'teaching_sections',
                  'assistant_sections',
                  'student_sections',
                  ]
        read_only_fields = ['username', ]


class UserPasswordUpdateSerializer(serializers.Serializer):
    old_pass = serializers.CharField(max_length=90, required=True, write_only=True)
    password = serializers.CharField(max_length=90, required=True, write_only=True)
    username = serializers.CharField(max_length=20, required=True, write_only=True)

    class Meta:
        fields = ['password', 'old_pass', 'username']

    def update(self, instance: User, validated_data):
        if not check_password(validated_data.pop('old_pass'), instance.password):
            raise serializers.ValidationError({'old_pass': 'not correct'})
        instance.password = make_password(validated_data.pop('password'))
        instance.save()
        return instance


class UserRegisterSerializer(serializers.Serializer):
    national_id = serializers.CharField(max_length=10)
    student_number = serializers.CharField(max_length=9)

    def create(self, validated_data):
        golestan_user = GolestanUser.objects.filter(
            student_number=validated_data.get('student_number'),
            national_id=validated_data.get('national_id'),
        ).first()
        if not golestan_user:
            raise serializers.ValidationError(
                'user does not exists in golestan or is registered before'
            )
        print(golestan_user.national_id)
        user = User.objects.create(
            first_name=golestan_user.first_name,
            last_name=golestan_user.last_name,
            username=golestan_user.student_number,
            national_id=golestan_user.national_id,
            password=make_password(golestan_user.national_id),
        )
        user.groups.add(Group.objects.filter(name='Student').first())
        user.save()

        golestan_user.delete()
