import random
import string
from django.shortcuts import get_object_or_404
from user.models import User
from user.models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework import viewsets, status
from django.dispatch import receiver

class UserViewSet(viewsets.ViewSet):
    def list(self, request): # GET /api/user
        queryset = list(User.objects.all().values())

        # Check if request contains any query parameters
        if request.query_params:
            # Get the value of the query parameter
            search = request.query_params.get('search', None)
            if search is not None:  
                # Search on the fields title, price, store
                queryset = list(User.objects.filter(username__icontains=search).values())
                queryset += list(User.objects.filter(name__icontains=search).values())
                queryset += list(User.objects.filter(suername__icontains=search).values())
                queryset += list(User.objects.filter(email__icontains=search).values())
                # Remove duplicates
                queryset = list({v['id']:v for v in queryset}.values())
        serializer = UserSerializer(queryset, many=True)
        
        return JsonResponse(queryset, safe=False, status=status.HTTP_200_OK)

    # TODO if time
    def register(self, request):
        pass

    def login(self, request):

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.data.get('username')
        password = serializer.data.get('password')
        user = get_object_or_404(User, username=username)
        if user.password == password:
            # Create a random 10 character string as a token
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

            # Return the token
            return JsonResponse({'token': token, "userId": user.id}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

            