from django.db.models.fields.files import FieldFile
from django.http import FileResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsRight
from api.serializers import IsLicenseValidResponseSerializer, IsLicenseValidSerializer, GetResourceSerializer, \
    ResponseResourceSerializer


# Create your views here.
class LicenseViewSet(GenericViewSet):
    permission_classes = [IsRight]

    @swagger_auto_schema(
        method='post',
        responses={200: IsLicenseValidResponseSerializer()},
        request_body=IsLicenseValidSerializer(),
    )
    @action(methods=['post'], detail=False)
    def is_valid(self, request):
        serializer = IsLicenseValidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.save().data)

    @swagger_auto_schema(
        method='post',
        responses={200: ResponseResourceSerializer()},
        request_body=GetResourceSerializer(),
    )
    @action(methods=['post'], detail=False)
    def resource(self, request):
        serializer = GetResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_data: FieldFile = serializer.save()

        return FileResponse(file_data, content_type='application/octet-stream')