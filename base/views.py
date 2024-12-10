from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RegistrationSerializer
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    output = f"Welcome {request.user.username}, Authentication Successful"
    return Response({'response': output}, status=status.HTTP_200_OK)

@api_view(["GET"])
def home(request):
    data = [
        'property 1',
        'property 2',
        'property 3'
    ]
    return Response(data)