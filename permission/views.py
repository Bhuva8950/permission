from django.shortcuts import render
from django.contrib.auth.models import User
from permission.serializers import *
from rest_framework import generics
from rest_framework.response import Response
from permission.models import MyUser
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from functools import wraps
# Create your views here.

def updatepermission():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            is_allow = request.request.user.is_allow
            if is_allow:
                return view(request, *args, **kwargs)
            return Response("You Dont have permission to update")
        return _wrapped_view
    return decorator

class CheckCreatePermission(BasePermission):

    def has_permission(self, request, view):
        is_allow = request.user.is_allow
        return True if is_allow else False

class HomeView(generics.ListCreateAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def list(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        data={"hello":"hello"}
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_staff = True
        user.set_password(request.data.get("password"))
        user.save()
        
        return Response(
            {"user":"user create"}
            )
    
    @updatepermission()
    def update(self, request, *args, **kwargs ):
        pk = self.kwargs.get("pk")
        instance = MyUser.objects.filter(id=pk).last()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message": f"Is allow permission give to user {instance.username}"})
            else:
                return Response({"message": "failed", "details": serializer.errors})
        except Exception as e :
            print(e)
            return Response({"message": "failed to give permission" })