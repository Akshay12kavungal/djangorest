from django.shortcuts import render
from .serializers import UserRegister,UserDataSerializer,FootballSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework import generics 


from rest_framework .filters import SearchFilter
from .models import Football


# Create your views here.

class register(APIView):
    def post(self,request,format=None):
        serializer=UserRegister(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']='registered'
            data['username']=account.username
            data['emai']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key

        else:
            data=serializer.errors

        return Response(data)

class welcome(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request):
        content={'user':str(request.user),'userid':str(request.user.id)}
        return Response(content)


class userdetails(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
           raise Http404
            

    def get(self,request,pk,format=None):
        userdata=self.get_object(pk)
        serializer=UserDataSerializer(userdata)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        userdata=self.get_object(pk)
        serializer=UserDataSerializer(userdata,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error','error':serializer.error})

    def delete(self,request,pk,format=None):
        userdata=self.get_object(pk)
        userdata.delete()
        return Response({"message":"user deleted"})

class setPagination(PageNumberPagination):
    page_size=2

class paginationApi(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserDataSerializer
    pagination_class=setPagination
    filter_backends=(SearchFilter,)
    search_fields=('username','email','first_name','last_name')


class FootballListCreate(generics.ListCreateAPIView):
    queryset=Football.objects.all()
    serializer_class=FootballSerializer
    pagination_class=setPagination
    filter_backends=(SearchFilter,)
    search_fields=('club_name','country_name','leage')
   


class FootballRetriveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=Football.objects.all()
    serializer_class=FootballSerializer
    field="pk"
    


