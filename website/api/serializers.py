from car_rent.models import Car
from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models import LANGUAGES, CustomUser


class CarSerializer(serializers.ModelSerializer):

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(self, *args, **kwargs)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['name'] = ret.get(f'name_{self.user.lang}')
        for lang in dict(LANGUAGES):
            ret.pop(f'name_{lang}', '')
        return ret

    class Meta:
        model = Car
        fields = ['name_ru', 'name_en', 'production_year', 'created_at', 'renter']


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'lang')


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, username, and password are required.
    Returns a JSON web token.
    """

    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'password', 'lang', 'token',)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }
