from rest_framework import serializers
from .models import Catsphone, Supplier


class CatphoneSerializers(serializers.ModelSerializer):
    class Meta:
        model = Catsphone
        fields = ['name', 'description', 'price', 'exist', 'supplier']
