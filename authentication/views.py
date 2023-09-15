from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, status
from django.shortcuts import get_object_or_404
from .serializers import (
    UserPasswordUpdateSerializer,
    UserSerializer,
)
from .models import (
    User,
)


class UserView(mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin,
               GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        obj = get_object_or_404(User, id=self.request.user.id)
        return obj


class UserChangePassView(GenericViewSet):
    serializer_class = UserPasswordUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = get_object_or_404(User, username=serializer.validated_data.get('username'))
        serializer.update(
            obj,
            serializer.validated_data
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED,)
