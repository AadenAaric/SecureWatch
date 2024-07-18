from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User,ActiveUser,Devices
from .serializers import UserSerializer, ActiveUserSerializer
import json
from .utils import hash_user_id
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from AI.CAMERA import VideoCamera
from shared_files.Camera_Initializer import rel,addCam
from video_streams.views import update_instances
    


def add_device(device_url):
    global camera_instances
    Dev = Devices()
    Dev.add_or_update_devices(device_url)


def delete_device(device_name):
    global camera_instances
    Devices.delete_device_by_name(name=device_name)

#testing api
def test(request):
    return HttpResponse(json.dumps({"message":"Working FIne!"}), content_type="application/json")

#testing page for Notifications
def notificationPanel(request):
    return render(request,"alert2.html", context = {  'name': 'World'})

#Login and Register ------------------------------------------------------------------------------------------
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Message":"User Registered Succesfully!","id":serializer.data['id']},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    csrf = get_token(request=request)
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email, password=password)
        hash = hash_user_id(user.id)
        ActSer = ActiveUserSerializer(data={"hashed_id":hash,"user_id":user.id,"is_active":"true"})
        if ActSer.is_valid():
           ActSer.save() 
           response = Response({
                "message": "Login Successful",
                "id": hash,
                "csrf":csrf
            }, status=status.HTTP_200_OK)
           #response.set_cookie(key='csrftoken', value=request.COOKIES.get('csrftoken'))
           return response
        return Response({"message": "DataBase Error!"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST'])
def logout(request):
        user = request.user
        user.delete()
        return Response({"message":"Successfully logged out!"},status=status.HTTP_200_OK)
    
    
#Updating, Fetching and Deleting devices----------------------------------------------------------------------------------

@api_view(['PUT'])
def update_device_urls(request):
    user_id = request.id
    user = get_object_or_404(User, pk=user_id)
    new_device_url = request.data.get('device_url')
    key, value = list(new_device_url.items())[0]
    Dev = Devices()
    if new_device_url:
        add_device(new_device_url)
        addCam(key,value)
        update_instances()
        return Response({"message":f"device added!{key,value}"},status=status.HTTP_200_OK)




@api_view(['PUT'])
def Add_get(request):
    user_id = request.id
    user = get_object_or_404(User,pk=user_id)
    devices = user.device_urls
    new_device_url = request.data.get('device_url')
    if new_device_url:
        user.device_urls.update(new_device_url)
        user.save()
        return Response(devices,status=status.HTTP_200_OK)
    return Response({"message":"Device Url not Provided!"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def Get_hashed(request):
    try:
        # Query the ActiveUser model to get all hashed_id values
        hashes = ActiveUser.objects.values_list('hashed_id', flat=True)
        
        # Convert the QuerySet to a list
        hashes_list = list(hashes)
        
        return Response(hashes_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def Get_device_urls(request):
    Dev = Devices()
    devices = Dev.get_Devices()
    return Response(devices,status=status.HTTP_200_OK)

@api_view(['DELETE'])
def Delete_device_url(request):
    name = request.data.get('key')
    if name:
        delete_device(device_name=name)
        rel(name)
        update_instances()
        return Response({"message":f"{name} successfully Deleted!"},status=status.HTTP_200_OK)
    return Response({"message":"Not Found!"},status=status.HTTP_400_BAD_REQUEST)
    
