
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Project API",
      default_version='v1',
      description="First version of API for this project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url="https://8000-firebase-zippycart-1769518988054.cluster-sumfw3zmzzhzkx4mpvz3ogth4y.cloudworkstations.dev/",
   
)

urlpatterns = [

    # admin login
    path('admin/', admin.site.urls),

    # drf urls
    path('api/drf/v1/', include('app.urls')),

    # swagger urls
    path('api/swagger/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # redoc urls
    path('api/redoc/v1/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),

]
