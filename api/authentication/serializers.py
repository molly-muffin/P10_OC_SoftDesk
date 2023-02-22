#############
# LIBRARIES #
#############
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers


#############
# VARIABLES #
#############
User = get_user_model()


#############
# FUNCTIONS #
#############
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    User characteristics
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {
                'required': True,
                'validators': [
                    UniqueValidator(queryset=User.objects.all(),
                    message="This email already exists !")
                ]
            },
            'password': {
                'required': True,
                'write_only': True,
                'validators': [validate_password]
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
