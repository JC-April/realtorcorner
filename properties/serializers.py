from rest_framework import serializers
from .models import Property, PropertyImage
from django.db import transaction

class PropertyImageSerializer(serializers.ModelSerializer):
    # include image url in serialized data
    url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            # generate full url for the image
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = ['id', 'property_name', 'slug', 'price', 'location', 'availability', 'purpose', 'contact', 'description', 'images', 'created_at', 'updated_at']

class PropertyCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)        
    #added the line below to handle image deletion
    remove_images = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)

    class Meta:
        model = Property
        fields = ['id', 'property_name', 'price', 'location', 'contact', 'availability', 'purpose', 'description', 'images', 'remove_images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')

        with transaction.atomic():
            property_instance = Property.objects.create(**validated_data)

            property_images = [PropertyImage(property=property_instance, image=image) for image in images_data]
            PropertyImage.objects.bulk_create(property_images)

        return property_instance
    
    # added this function
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        remove_images_data = validated_data.pop('remove_images', [])

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            PropertyImage.objects.filter(id__in=remove_images_data).delete()

            # add new images if provided
            if images_data:
                property_images = [PropertyImage(property=instance, image=image) for image in images_data]
                PropertyImage.objects.bulk_create(property_images)

        return instance