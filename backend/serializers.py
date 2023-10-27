from rest_framework import serializers
from .models import Device, TemperatureReading, HumidityReading


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"  # Include all fields from the Device model


class TemperatureReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureReading
        fields = "__all__"  # Include all fields from the TemperatureReading model


class HumidityReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumidityReading
        fields = "__all__"  # Include all fields from the HumidityReading model
