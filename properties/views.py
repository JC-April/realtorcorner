from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Property, PropertyImage
from .serializers import PropertySerializer, PropertyCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.db.models import Q
from django.db import transaction

# Create your views here.

@api_view(["GET"])
def property_list(request):
        properties = Property.objects.all()

        # Get filtering parameters from the request
        purpose = request.GET.get('purpose')
        availability = request.GET.get('availability')
        location = request.GET.get('location')
        property_name = request.GET.get('property_name')

        # Apply filters 
        if purpose:
            properties = properties.filter(purpose=purpose)
        if availability:    
            properties = properties.filter(availability=availability)
        if location:
            properties = properties.filter(location__icontains=location)
        if property_name:
            words = property_name.split()
            name_filter = Q()
            for word in words:
                # Add an OR filter. filter by each word, then combine
                name_filter |= Q(property_name__icontains=word)
            properties = properties.filter(name_filter)

        serializer = PropertySerializer(properties, many=True, context={'request': request})
        return Response(serializer.data)

@api_view(["GET"])
def property_detail(request, slug):
     property_instance = get_object_or_404(Property, slug=slug)
     serializer = PropertySerializer(property_instance, context={'request': request})
     return Response(serializer.data)
    
@api_view(["GET"])
@permission_classes([IsAdminUser])
def dashboard(request):
    properties = Property.objects.filter(owner=request.user)

    # Get filtering parameters from the request
    purpose = request.GET.get('purpose')
    availability = request.GET.get('availability')
    location = request.GET.get('location')
    property_name = request.GET.get('property_name')

    # Apply filters 
    if purpose:
        properties = properties.filter(purpose=purpose)
    if availability:    
        properties = properties.filter(availability=availability)
    if location:
        properties = properties.filter(location__icontains=location)
    if property_name:
            words = property_name.split()
            name_filter = Q()
            for word in words:
                # Add an OR filter. filter by each word, then combine
                name_filter |= Q(property_name__icontains=word)
            properties = properties.filter(name_filter)

    serializer = PropertySerializer(properties, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def create_property(request):
    
    serializer = PropertyCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
def property_edit(request, slug):
    property_instance = get_object_or_404(Property, slug=slug, owner=request.user)

    if request.method == 'GET':
        # View details of a specific property
        serializer = PropertySerializer(property_instance)
        return Response(serializer.data)

    if request.method == "PUT":
    
        serializer = PropertyCreateSerializer(property_instance, data=request.data, partial=True)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    if request.method == "DELETE":

        property_instance.delete()
        return Response({"message": "Property deleted successfully"}, status=status.HTTP_204_NO_CONTENT)    


