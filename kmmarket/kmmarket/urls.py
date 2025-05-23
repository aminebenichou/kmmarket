"""
URL configuration for kmmarket project.

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store.views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("catgeories", CategoryViewSet) 
router.register("seller", SellerViewSet)
router.register("client", ClientViewSet)
router.register("ratings", RatingViewSet)
router.register("orders", OrderViewSet)
router.register("signUp", UserViewset)
router.register("tracking", TrackingViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.obtain_auth_token),
    path('userInfo', getUserInfo),
    # path('get-tracking/', getTracking),
    path("", include(router.urls))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)