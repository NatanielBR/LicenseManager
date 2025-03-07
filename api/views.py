from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import IsLicenseValidResponseSerializer, IsLicenseValidSerializer, GetResourceSerializer, \
    ResponseResourceSerializer


# Create your views here.
class LicenseViewSet(GenericViewSet):

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
        responses={200: GetResourceSerializer()},
        request_body=ResponseResourceSerializer(),
    )
    @action(methods=['post'], detail=False)
    def resource(self, request):
        serializer = GetResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.save().data)