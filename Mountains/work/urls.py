"""
URL configuration for work project.

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
from django.urls import path, include
from rest_framework import routers
from passage.views import LevelViewSet, PerevalViewSet, UserViewSet, CoordViewSet, ImageViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'levels', LevelViewSet)
router.register(r'coords', CoordViewSet, basename='coords')
router.register(r'images', ImageViewSet)
router.register(r'submitData', PerevalViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]