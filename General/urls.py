from django.urls import path
from .  import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("test",views.test),
    path("np",views.notificationPanel,name="notificationPanel"),
    path("register",views.register,name="Register"),
    path("login",views.login,name="Login"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("updatedevices",views.update_device_urls,name="update_device_urls"),
    path("getDevicesurl",views.Get_device_urls,name="Get_devies urls"),
    path("deleteDevice",views.Delete_device_url,name="Delete_device_url"),
]