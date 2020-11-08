from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from car_rent.models import Car
from users.models import CustomUser

from .serializers import (CarSerializer, CustomUserSerializer, LoginSerializer,
                          RegistrationSerializer)

User = get_user_model()


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCarsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CarSerializer

    def get(self, request):
        queryset = Car.objects.filter(renter=request.user)
        cars = CarSerializer(queryset, many=True)
        return Response(cars.data)

class AdminCarsView(UserCarsView):
    permission_classes = (IsAdminUser, )

    def get(self, request, user_pk):
        try:
            user = User.objects.get(pk=int(user_pk))
        except Exception as e:
            return Response({'exception': e})
        queryset = Car.objects.filter(renter=user)
        cars = CarSerializer(queryset, many=True)
        return Response(cars.data)

class GetAllUsers(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        queryset = User.objects.all()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, user_pk):
        try:
            user = User.objects.get(pk=int(user_pk))
        except Exception as e:
            return Response({'exception': e})
        return Response(CustomUserSerializer(user).data)

    def put(self, request, user_pk):
        try:
            user = User.objects.get(pk=int(user_pk))
        except Exception as e:
            return Response({'exception': e})

        new_data = json.loads(request.body.decode())
        serializer = CustomUserSerializer(user, data=new_data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            return Response(CustomUserSerializer(obj).data)
