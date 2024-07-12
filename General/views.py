from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import UserSerializer
import json


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
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email,password=password)
        return Response({"message":"Login Successfull","id":user.id},status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message":"Invalid Credentials"},status=status.HTTP_401_UNAUTHORIZED)
    

    
#Updating, Fetching and Deleting devices----------------------------------------------------------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_device_urls(request):
    user_id = request.headers.get('id')
    user = get_object_or_404(User, pk=user_id)
    new_device_url = request.data.get('device_url')
    if new_device_url:
        user.device_urls.update(new_device_url)
        user.save()
        return Response({"message":"device added!"},status=status.HTTP_200_OK)
    return Response({"message":"Device Url not Provided!"},status=status.HTTP_400_BAD_REQUEST)


    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_device_urls(request):
    user_id = request.headers.get('id')
    user = get_object_or_404(User,pk=user_id)
    devices = user.device_urls
    return Response(devices,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Delete_device_url(request):
    user_id = request.headers.get('id')
    user = get_object_or_404(User,pk=user_id)
    device = request.data.get('key')
    if user.device_urls:
        if device in user.device_urls:
          del user.device_urls[device]
          user.save()
          return Response({"message":f"{device} successfully Deleted!"},status=status.HTTP_200_OK)
        return Response({"message":"Not Found!"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"No Device!"},status=status.HTTP_400_BAD_REQUEST)
    
