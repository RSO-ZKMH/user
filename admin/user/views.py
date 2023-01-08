from django.shortcuts import get_object_or_404
from user.models import User
from user.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from constance import config
from constance.signals import config_updated
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

    def retrieve(self, request, pk=None): # GET /api/user/:id
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(operation_description="Create a user", responses={404: 'slug not found'})
    def create(self, request): # POST /api/user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None): # PUT /api/user/:id
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None): # DELETE /api/user/:id
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        