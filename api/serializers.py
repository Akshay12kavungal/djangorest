from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Football

User=get_user_model()

class UserRegister(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=["username","password","email","password2"]

    def save(self):
        reg=User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']


        if password!=password2:
            raise serializers.ValidationError({'password':'password does not match'})
        reg.set_password(password)
        reg.save()
        return reg
class UserDataSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['username','email','first_name','last_name']


class FootballSerializer(serializers.ModelSerializer):
    class Meta:
        model=Football
        fields=['club_name','country_name','leage']

    def create(self,validated_data):
        existing=Football.objects.filter(club_name=validated_data['club_name']).first()
        
        if existing:
         
            raise serializers.ValidationError("A Football object with this club name already exists.")
        else:
            return Football.objects.create(**validated_data)






   