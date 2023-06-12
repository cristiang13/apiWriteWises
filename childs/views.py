from django.shortcuts import render
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from .models import Childs
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse



# Create your views here.
class AddChild(APIView):
    @async_to_sync
    async def post(self,request):
        try:
            child_data = {
                "child_name" : request.data['childName'],
                "age" : request.data['childAge'],
                "childcare" : request.data['childCare'],
                "childcare_worker": request.data['token']
            }
            child_id = Childs.create(child_data).inserted_id
            return Response({"message": 'Added child'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class GetChilds(APIView):
    @async_to_sync
    async def post(self,request):
        try:
            childcareworker_id = request.data['token']
            childs = Childs.get_by_childcareworker(childcareworker_id)
            
            return Response({"data": childs}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        