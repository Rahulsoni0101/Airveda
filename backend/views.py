from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from rest_framework.decorators import api_view
from .models import Device, TemperatureReading, HumidityReading
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO
import base64

# Create your views here.
from rest_framework import generics
from .models import Device, TemperatureReading, HumidityReading
from .serializers import (
    DeviceSerializer,
    TemperatureReadingSerializer,
    HumidityReadingSerializer,
)


class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDeleteView(APIView):
    def delete(self, request, device_uid, format=None):
        try:
            device = Device.objects.get(uuid=device_uid)
        except Device.DoesNotExist:
            return Response(
                {"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND
            )

        device.delete()
        return Response({"detail": "Device deleted"}, status=status.HTTP_204_NO_CONTENT)


class DeviceRetrieveView(APIView):
    def get(self, request, device_uid, format=None):
        try:
            device = Device.objects.get(uuid=device_uid)
        except Device.DoesNotExist:
            return Response(
                {"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = DeviceSerializer(device)
        return Response(serializer.data)


class DeviceListAllView(APIView):
    def get(self, request, format=None):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)


class DeviceReadingsView(APIView):
    def get(self, request, device_uid, parameter, format=None):
        start_on = request.query_params.get("start_on")
        end_on = request.query_params.get("end_on")

        try:
            start_on_dt = datetime.strptime(start_on, "%Y-%m-%dT%H:%M:%S")
            end_on_dt = datetime.strptime(end_on, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return Response(
                {"detail": "Invalid datetime format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if parameter not in ["temperature", "humidity"]:
            return Response(
                {"detail": "Invalid parameter"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            device = Device.objects.get(uuid=device_uid)
        except Device.DoesNotExist:
            return Response(
                {"detail": "Device not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if parameter == "temperature":
            readings = TemperatureReading.objects.filter(
                device__uuid=device_uid,
                timestamp__gte=start_on_dt,
                timestamp__lte=end_on_dt,
            )
        else:
            readings = HumidityReading.objects.filter(
                device__uuid=device_uid,
                timestamp__gte=start_on_dt,
                timestamp__lte=end_on_dt,
            )

        if readings:
            if parameter == "temperature":
                serializer = TemperatureReadingSerializer(readings, many=True)
            else:
                serializer = HumidityReadingSerializer(readings, many=True)
            serialized_data = serializer.data

            response_data = {"device_name": device.name, "readings": serialized_data}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "No data found"}, status=status.HTTP_404_NOT_FOUND
            )


def plot_device_readings(request):
    device_uid = request.GET.get("device_uid")

    try:
        device = Device.objects.get(uuid=device_uid)
        temperature_readings = TemperatureReading.objects.filter(device=device)
        humidity_readings = HumidityReading.objects.filter(device=device)
    except Device.DoesNotExist:
        return render(request, "error.html", {"error_message": "Device not found"})

    timestamps = [reading.timestamp for reading in temperature_readings]
    temperatures = [reading.temperature for reading in temperature_readings]
    humidities = [reading.humidity for reading in humidity_readings]

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, temperatures, label="Temperature", marker="o")
    plt.plot(timestamps, humidities, label="Humidity", marker="o")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.title(f"Device {device.name} - Temperature and Humidity Readings")
    plt.xticks(rotation=45)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    graph = base64.b64encode(buf.read()).decode("utf-8")

    return render(request, "graph.html", {"graph": graph})
