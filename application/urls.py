"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Swagger",
        default_version="v1",
        description="Swagger",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/devices/", views.DeviceListCreateView.as_view(), name="device-list-create"
    ),
    path(
        "api/devices/<uuid:device_uid>/",
        views.DeviceDeleteView.as_view(),
        name="device-retrieve-update-delete",
    ),
    path(
        "api/devices-get/<uuid:device_uid>/",
        views.DeviceRetrieveView.as_view(),
        name="device-retrieve",
    ),
    path(
        "api/devices-all/",
        views.DeviceListAllView.as_view(),
        name="device-retrieve-all",
    ),
    path(
        "api/devices/<uuid:device_uid>/readings/<str:parameter>/",
        views.DeviceReadingsView.as_view(),
        name="device-readings",
    ),
    path("devices-graph/", views.plot_device_readings, name="device-readings-graph"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
