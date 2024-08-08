from django.urls import path
from .  import views
from shared_middlewares.authentication import AuthenticationMiddleware

urlpatterns = [
    path("test",views.test),
    path("np",views.notificationPanel,name="notificationPanel"),
    path("register",views.register,name="Register"),
    path("login",views.login,name="Login"),
    path("updatedevices",AuthenticationMiddleware(views.update_device_urls),name="update_device_urls"),
    path("getDevicesurl",AuthenticationMiddleware(views.Get_device_urls),name="Get_devies urls"),
    path("deleteDevice",AuthenticationMiddleware(views.Delete_device_url),name="Delete_device_url"),
    path("gethashes",AuthenticationMiddleware(views.Get_hashed),name="GetHash"),
    path("logout",AuthenticationMiddleware(views.logout),name="logout"),
    path("addget",AuthenticationMiddleware(views.Add_get),name="aDDGET"),
    path('', views.index, name = 'index'),
    path('upload', views.fileupload, name = "File_Uploads"),
    path('uploadapi', views.fileuploadapi, name = "File_Uploads"),
    path('sendToken',AuthenticationMiddleware(views.getDeviceToken), name="SendToken" ),
    path('gallery', views.image_gallery, name='image_gallery'),
    path('deleteImage', views.deleteImage, name='deleteimage'),
    path('GetTrainedData', views.GetTrainedNames, name='GetTrainedData'),

]