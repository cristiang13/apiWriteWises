
import json
import os
import asyncio
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
from rest_framework.views import APIView
from utils import utils
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import openai
from dotenv import load_dotenv
load_dotenv()


@sync_to_async
def create_chat_completion(*args, **kwargs):
    return openai.ChatCompletion.create(*args, **kwargs)

class ChatView(APIView):
    @async_to_sync
    async def post(self,request):
        user_message = request.data.get('message', '')
        previous_messages = request.data.get('messages', [])

        openai.api_key= os.getenv("OPENAI_API_KEY")
        try:
            response = await create_chat_completion(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    *previous_messages,
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                max_tokens=800,
                n=1,
                temperature=0.7,
                timeout=180,
            )
        except asyncio.TimeoutError:
            return Response({'message': 'Error: Request timed out. Please try again later.'})
        ai_message = response.choices[0].message['content'].strip()
        return  Response({'message': ai_message})

class ChatToDoAustraliaView(APIView):
    @async_to_sync
    async def post(self,request):
        user_message = request.data.get('message', '')
        modified_request = utils.modify_to_do_australia(request)
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_request.content)
       
        openai.api_key= os.getenv("OPENAI_API_KEY")
        try:
            response = await create_chat_completion(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": modified_request_dict['message']
                    }
                ],
                max_tokens=800,
                n=1,
                temperature=0.3,
                timeout=180,
                frequency_penalty=0,
                presence_penalty=0,
            )
        except asyncio.TimeoutError:
            return Response({'message': 'Error: Request timed out. Please try again later.'})
        ai_message = response.choices[0].message['content'].strip()
        return  Response({'message': ai_message})

# Crea una función para manejar la solicitud de cada opción
async def async_process_request(request):
    print("entrando a funcion chatgpt")
    user_message = request["message"]
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = await asyncio.wait_for(create_chat_completion(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=1000,
            n=1,
            temperature=0.1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            timeout=180,
        ), timeout=180)

        if 'variables' in request:
            new_dict = {
                    'variables': request['variables'],
                    'token': request['token'],
                    'type_report':request['type_report'],
                    'response_chatgpt': response.choices[0].message['content'].strip()
            }
            utils.save_variables_report(new_dict)
    except asyncio.TimeoutError:
        return Response({'message': 'Error: Request timed out. Please try again later.'})



    ai_message = response.choices[0].message['content'].strip()
   
    return Response({'message': ai_message})


class DailyReportView(APIView):
    @async_to_sync
    async def post(self,request):
        # request.data['cancellation_token_id'] = token_id
        modified_response = utils.modify_request(request) 
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_response.content)
        print("preparandose para enviar datos a openai")
        return await async_process_request( modified_request_dict)


class GoalReportView(APIView):
    @async_to_sync
    async def post(self,request):
    
        modified_response = utils.modify_goal_request(request) 
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_response.content)
       
        return await async_process_request( modified_request_dict)


class ObservationsReportView(APIView):
    @async_to_sync
    async def post(self,request):
        modified_response = utils.modify_observation_request(request) 
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_response.content)
        
        return await async_process_request( modified_request_dict)

class CriticalReflectionsReportView(APIView):
    @async_to_sync
    async def post(self,request):
        modified_response= utils.modify_critical_reflection_request(request)
        modified_request_dict = json.loads(modified_response.content)
        return await async_process_request( modified_request_dict)


class WeeklyReflection(APIView):
    @async_to_sync
    async def post(self,request):
        modified_response = utils.modify_weeklyReflection_request(request) 
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_response.content)
       
        return await async_process_request( modified_request_dict) 
        
       
class WeeklyPlanning(APIView):
    @async_to_sync
    async def post(self,request):
        modified_response = utils.modify_weeklyPlanning_request(request) 
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_response.content)
       
        return await async_process_request( modified_request_dict) 

# from report
class SaveReport(APIView):
    @async_to_sync
    async def post(self,request):
        try:
            save_report= utils.save_report(request)
            return Response({"message": "Save report exit"}, status=status.HTTP_201_CREATED) 
        except :
            return Response({"message": "Not Save report exit"}, status=status.HTTP_400_BAD_REQUEST) 

class HistoricalReport(APIView):
    @async_to_sync
    async def post(self,request):
        historical_reports= utils.historical_reports(request)
        modified_request_dict = json.loads(historical_reports.content)
        return Response({"list_report": modified_request_dict}, status=status.HTTP_201_CREATED) 
    
class GetHistoricalReport(APIView):
    @async_to_sync
    async def post(self, request):
        try:
            get_report= utils.historical_report(request)
            modified_request_dict = json.loads(get_report.content)
            return Response({"get_report": modified_request_dict}, status=status.HTTP_201_CREATED)
        except :
            return Response({"message": "There is no report"}, status=status.HTTP_400_BAD_REQUEST) 

class  GetVariablesReports(APIView):
    @async_to_sync
    async def post(self,request):
        try:
            get_report= utils.get_variables_reports(request)
            modified_request_dict = json.loads(get_report.content)
            return Response({"get_report": modified_request_dict}, status=status.HTTP_201_CREATED)
        except :
            return Response({"message": "There is no variables"}, status=status.HTTP_400_BAD_REQUEST) 

class DaysToWeeklyReflection(APIView):
    @async_to_sync
    async def post(self,request):
        try:
            get_report= utils.modify_days_to_weekly_reflection(request)
            modified_request_dict = json.loads(get_report.content)
            return await async_process_request(modified_request_dict)
        except :
            return Response({"message": "Error in weekly reflection by days"}, status=status.HTTP_400_BAD_REQUEST)

class FollowUp(APIView):
    @async_to_sync
    async def post(self,request):
        modified_response = utils.modify_follow_up_request(request) 
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_response.content)
        return await async_process_request( modified_request_dict) 

class GetLastVariableReport(APIView):
    @async_to_sync
    async def post(self,request):
        modified_response = utils.modify_get_last_variable_report(request) 
        # Extraer el diccionario del objeto JsonResponse
        modified_request_dict = json.loads(modified_response.content)
        return Response({"get_variables": modified_request_dict}, status=status.HTTP_201_CREATED)

class CreateWord(APIView):
    @async_to_sync
    async def post(self,request):
        data = request.data
        link_doc = utils.modify_create_word(data)
        return  Response({'message': link_doc}, status=status.HTTP_201_CREATED)

            
chat= ChatView.as_view()
daily_report = DailyReportView.as_view()
goal_report = GoalReportView.as_view()
observations_report = ObservationsReportView.as_view()
critical_reflection = CriticalReflectionsReportView.as_view()
to_do_australia= ChatToDoAustraliaView.as_view()
save_report= SaveReport.as_view()
historical_report=HistoricalReport.as_view()
weekly_reflection = WeeklyReflection.as_view()
weekly_planning = WeeklyPlanning.as_view()
get_historical_report= GetHistoricalReport.as_view()
get_variables_reports= GetVariablesReports.as_view()
days_to_weekly_reflection = DaysToWeeklyReflection.as_view()
follow_up = FollowUp.as_view()
get_last_variable_report= GetLastVariableReport.as_view()
create_word = CreateWord.as_view()

