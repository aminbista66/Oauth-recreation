from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenVerifySerializer

class TestView(GenericAPIView):
    authentication_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = self.request.META['Authorization'].split(' ')[0]
        serializer = TokenVerifySerializer()
        serializer.validate({"token": token})
        return Response({"status": 'authorized'})