from django.shortcuts import render
from api.serializer import userserializer,Quesserializer,Answserializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from api.models import Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.decorators import action

class Usersview(ModelViewSet):
    serializer_class=userserializer
    queryset=User.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class Questionsview(ModelViewSet):
    serializer_class=Quesserializer
    queryset=Questions.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    @action(methods=["GET"],detail=False)
    def myques(self,request,*args,**kwargs):
        qs=request.user.questions_set.all()
        serializer=Quesserializer(qs,many=True)
        return Response(data=serializer.data)
    @action(methods=["GET"],detail=True)
    def list_ques(self,request,*arg,**kw):
        id=kw.get("pk")
        ques=Questions.objects.get(id=id)
        qs=ques.answers_set.all()
        serializer=Answserializer(qs,many=True)
        return Response(data=serializer.data)
    
class Answerview(ModelViewSet):
    serializer_class=Answserializer
    queryset=Answers.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    @action(methods=["post"],detail=True)
    def add_answer(self,request,*ar,**kw):
        id=kw.get("pk")
        ques=Questions.objects.get(id=id)
        usr=request.user
        serilaizer=Answserializer(data=request.data,context={"question":ques,"user":usr})
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(data=serilaizer.data)
        else:
            return Response(data=serilaizer.errors) 
    @action(methods=["get"],detail=True)
    def upvote(self,request,*ar,**kw):
        ans=self.get_object()
        usr=request.user
        ans.upvote.add(usr)
        return Response(data="created")
    
