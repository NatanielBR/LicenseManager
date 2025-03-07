import base64

from django.utils import timezone
from rest_framework import serializers

from api.models import Application, Client, Resource


class IsLicenseValidSerializer(serializers.Serializer):
    application_id = serializers.CharField(max_length=254)
    license_id = serializers.CharField(max_length=254)

    def validate_application_id(self, value):
        application_query = Application.objects.filter(id=value)
        if not application_query.exists():
            raise serializers.ValidationError('Application not found')
        return value

    def validate_license_id(self, value):
        license_query = Client.objects.filter(id=value, application__in=[self.initial_data['application_id']])
        if not license_query.exists():
            raise serializers.ValidationError('License not found')
        return value

    def save(self) -> 'IsLicenseValidResponseSerializer':
        client = Client.objects.get(id=self.validated_data['license_id'])
        is_valid = False
        if timezone.now() < client.valid_until:
            is_valid = True

        return IsLicenseValidResponseSerializer(
            instance={
                'status': is_valid,
                'valid_until': client.valid_until.isoformat()
            }
        )


class IsLicenseValidResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    valid_until = serializers.DateTimeField()


class GetResourceSerializer(serializers.Serializer):
    application_id = serializers.CharField(max_length=254)
    license_id = serializers.CharField(max_length=254)
    resource_id = serializers.CharField(max_length=254)

    def validate_application_id(self, value):
        application_query = Application.objects.filter(id=value)
        if not application_query.exists():
            raise serializers.ValidationError('Application not found')
        return value

    def validate_license_id(self, value):
        query = Client.objects.filter(id=value, application__in=[self.initial_data['application_id']])
        if not query.exists():
            raise serializers.ValidationError('License not found')
        return value

    def validate_resource_id(self, value):
        query = Resource.objects.filter(id=value, application__in=[self.initial_data['application_id']])
        if not query.exists():
            raise serializers.ValidationError('Resource not found')
        return value

    def save(self) -> 'ResponseResourceSerializer':
        resource = Resource.objects.get(
            id=self.validated_data['resource_id'],
            application__in=[self.initial_data['application_id']]
        )


        return ResponseResourceSerializer(
            instance={
                'resource_id': resource.id,
                'resource': base64.b64encode(resource.data.read()).decode()
            }
        )


class ResponseResourceSerializer(serializers.Serializer):
    resource_id = serializers.CharField(max_length=254)
    resource = serializers.CharField()
