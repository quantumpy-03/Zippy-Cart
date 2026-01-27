
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import CreateUserSerializers, UserProfileSerializer, ChangeUserPasswordSerializer



class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializers
    permission_classes = [AllowAny]

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserAccountDeleteView(DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangeUserPasswordView(APIView):
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated]
 
    @swagger_auto_schema(request_body=ChangeUserPasswordSerializer)
    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = ChangeUserPasswordSerializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
