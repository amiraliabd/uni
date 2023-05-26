from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, status
from rest_framework.decorators import action
from .serializers import (
    UserPasswordUpdateSerializer,
    UserSerializer,
    UserRegisterSerializer,
)
from core.serializers import UserSectionSerializer
from .models import (
    User,
)


class UserView(mixins.UpdateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.filter(is_superuser=False).all()

    @action(detail=False,
            methods=['post', ],
            permission_classes=[AllowAny, ]
            )
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['get', ],
            serializer_class=UserSectionSerializer,
            )
    def student_sections(self, request, pk=None):
        user = self.get_object()
        serializer = UserSectionSerializer(
            UserSectionSerializer.student_sections(user),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True,
            methods=['get', ],
            serializer_class=UserSectionSerializer,
            )
    def assistant_sections(self, request, pk=None):
        user = self.get_object()
        serializer = UserSectionSerializer(
            UserSectionSerializer.assistant_sections(user),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True,
            methods=['get', ],
            serializer_class=UserSectionSerializer,
            )
    def teaching_sections(self, request, pk=None):
        user = self.get_object()
        serializer = UserSectionSerializer(
            UserSectionSerializer.teaching_sections(user),
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class UserChangePassView(GenericViewSet):
    serializer_class = UserPasswordUpdateSerializer
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            User.objects.filter(username=serializer.validated_data.get('username')).first(),
            serializer.validated_data
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED,)
