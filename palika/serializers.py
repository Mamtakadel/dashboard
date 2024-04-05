from rest_framework import serializers

from palika.models import UserAuth

#serializers to signup
class SignUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'
        