from rest_framework.serializers import ModelSerializer
from .models import *

class StdSer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"