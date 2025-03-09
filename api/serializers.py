import base64

from django.core.signing import Signer
from django.utils import timezone
from rest_framework import serializers

from api.models import Application, Client, Resource


class IsLicenseValidSerializer(serializers.Serializer):
    application_id = serializers.CharField(max_length=254)
    license_id = serializers.CharField(max_length=254)
    machine_id = serializers.CharField(max_length=254)

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

    def validate_machine_id(self, value):
        if value == '' or value is None:
            raise serializers.ValidationError('Machine ID is required')

        client_query = Client.objects.filter(
            id=self.initial_data['license_id'],
            application__in=[self.initial_data['application_id']]
        )
        if not client_query.exists():
            raise serializers.ValidationError('License not found')

        client: Client = client_query.first()

        if not client.machine_lock:
            return value

        if client.machine_id == '':
            client.machine_id = value
            client.save()
        elif client.machine_id != value:
            raise serializers.ValidationError('Machine ID unmatched')

        return value

    def save(self) -> 'IsLicenseValidResponseSerializer':
        client = Client.objects.get(id=self.validated_data['license_id'])
        is_valid = False
        if timezone.now() < client.valid_until:
            is_valid = True

        if is_valid:
            signer = Signer()
            license = signer.sign_object([
                str(self.validated_data['license_id'], ),
                str(self.validated_data['application_id'], ),
                str(self.validated_data['machine_id'], )
            ])
        else:
            license = ''

        return IsLicenseValidResponseSerializer(
            instance={
                'status': is_valid,
                'auth_token': license,
                'valid_until': client.valid_until.isoformat()
            }
        )


class IsLicenseValidResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField()
    auth_token = serializers.CharField()
    valid_until = serializers.DateTimeField()


class GetResourceSerializer(serializers.Serializer):
    auth_token = serializers.CharField(max_length=254)
    resource_id = serializers.CharField(max_length=254)

    def validate_auth_token(self, value):
        signer = Signer()
        try:
            # ['license_id', 'application_id','machine_id']
            auth_token = signer.unsign_object(value)
        except Exception:
            raise serializers.ValidationError('Invalid auth token')

        license_id, application_id, machine_id = auth_token

        query = Client.objects.filter(
            id=license_id, application__in=[application_id]
        )

        if not query.exists():
            raise serializers.ValidationError('License invalid')

        client = query.first()

        if not client.machine_lock:
            # allow access to any machine
            return value

        if client.machine_id != machine_id:
            raise serializers.ValidationError('License invalid')

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
