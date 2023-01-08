from django.urls import path
from user.views import UserViewSet
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
import os


class PublicAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        # Get env variable
        base_path = os.getenv('BASE_PATH', '')
        schema.base_path = base_path+'/api/v1'
        return schema


schema_view = swagger_get_schema_view(
    openapi.Info(
        title="User API",
        default_version='1.0.0',
        description="API Documentation for user",
    ),
    public=True,
    generator_class=PublicAPISchemeGenerator
)

urlpatterns = [
    path('user', UserViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('user/<str:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
        'patch': 'partial_update',
    })),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
