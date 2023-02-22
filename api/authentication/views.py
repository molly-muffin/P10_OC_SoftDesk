#############
# LIBRARIES #
#############
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status



#############
# VARIABLES #
#############
User = get_user_model()


#############
# FUNCTIONS #
#############
class UserRegistrationView(CreateAPIView):
    """
    View for user creation
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({'User': UserRegistrationSerializer(user, context=self.get_serializer_context()).data,
                             'Message': "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


