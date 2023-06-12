
from datetime import datetime
import os
import json
import re
from users.models import User
from utils.dbmongo.historical_report_mongo import HistoricalReportMongo
from utils.dbmongo.variables_report import VariablesReport
from pathlib import Path
from django.http import JsonResponse
from dotenv import load_dotenv
load_dotenv()
from django.conf import settings
import uuid
import asyncio
from bson import ObjectId
from docxtpl import DocxTemplate
from django.http import FileResponse

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from docx.enum.text import WD_BREAK
from oauth2client.service_account import ServiceAccountCredentials




# ESCRIBIR LA UBICACION DEL ARCHIVO JSON

path_file = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'json', 'OpenAi_B.json'))
path_file_word = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'file', 'FormatoObservation.docx'))

cancellation_tokens = {}

def dateYYMMDD(date):
    # Formatea el objeto datetime a una cadena con solo la fecha
    date_only_str = date.strftime("%Y-%m-%d")
    return date_only_str

def variables_chatgpt(option):
    variables_chatgpt="null"

    with open(path_file,encoding="utf-8") as json_file:
        data = json.load(json_file)
    if option in list(data[0].keys()):
        variables_chatgpt= data[0][option]
        print("opcion esta dentro de lista")  
    
    return variables_chatgpt 

def modify_request(request):
    # Convertir el objeto JSON en un diccionario de Python
    request_dict = request.data

    variables = {
        'date': request_dict['date'],
        'range_age': request_dict['rangeAgeDailyReport'],
        'activities': request_dict['activities']
    }
    # Crear un nuevo diccionario con los cambios deseados 
    new_dict = {
        'message': f"age: {request_dict['rangeAgeDailyReport']}, activities {request_dict['activities']} /n with the previus text and based on each activity Write in English a long description of the day mentioning The physical, gross, fine motor, social, cognitive and language skills that children develop with each activity",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'daily_report',
    
    }
    return  JsonResponse(new_dict)

def modify_to_do_australia(request):
    request_dict = request.data
    print("modifique to do australia",request_dict['message'])
     # Crear un nuevo diccionario con los cambios deseados
    new_dict = {
        'message': f"I want you to act as an expert in topic related to Australia, providing comprehensive information on various aspects. I will give you a topic and you will answer in the same language that I asked. write detailed step by step {request_dict['message']} and write 5 link to find more information."
    }
    return  JsonResponse(new_dict)

def modify_goal_request(request):
    # Convertir el objeto JSON en un diccionario de Python
    request_dict = request.data
    variables = {
        'date': request_dict['date'],
        'name': request_dict['name'],
        'age': request_dict['age'],
        'goals': request_dict['goals']
    }
    # Crear un nuevo diccionario con los cambios deseados
    new_dict = {
        'message': f" date: {request_dict['date']}, name: {request_dict['name']}, Goal: {request_dict['goals']}./nI want you to act as a child care teacher of {request_dict['name']} with {request_dict['age']}  years using developmental milestones NQS and EYLF, PLANNING CYCLE, PRINCIPLES, PRACTICES and LEARNING OUTCOMES of the Early Years Learning Framework (EYLF) /n in English write a title suitable to the goal 1.write the goal longer and professional, 2. 3 strategies suitable for the goal, 3. 3 activities suitable for the goal, 4. 3 EYLF practices suitable for the goal, 5. 3 EYLF principle suitable for the goal, 6. describe 2 EYLF outcomes with sub-outcomes suitable for the goal, 7. 2 NQS with sub-elements suitable for the goal, 8. 3 developmental area for the goal",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'goal_report',
    
    }
    return  JsonResponse(new_dict)

def modify_observation_request(request):
    # Convertir el objeto JSON en un diccionario de Python
    request_dict = request.data

    variables = {
        'date': request_dict['date'],
        'name': request_dict['name'],
        'age': request_dict['age'],
        'descriptions': request_dict['descriptions'],
        'goal_observations': request_dict['goalObservations']
        
    }
    # date,name,age,goalObservations,descriptions  
    new_dict = {
        'message': f"date: {request_dict['date']}, goal: {request_dict['goalObservations']}, /n Name: {request_dict['name']}, /n age {request_dict['age']}, /n Description: {request_dict['descriptions']} /n from the previous text write in English 1description: write a long observation about description, 2Analysis: write five detailed analysis between the goal and description, 3What is next: create a future activity related to the description,4EYLF Learning Outcomes and sub-Outcomes suitable",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'descriptions_report',
    }
    return  JsonResponse(new_dict)

def modify_follow_up_request(request):
    # Convertir el objeto JSON en un diccionario de Python
    request_dict = request.data

    variables = {
        'date': request_dict['date'],
        'name': request_dict['name'],
        'age': request_dict['age'],
        'descriptions': request_dict['descriptionsFollowUp'],
        'goals': request_dict['goalFollowUp']
    }
    # date,name,age,goalObservations,descriptions 
    new_dict = {
        'message': f"date: {request_dict['date']}, goal: {request_dict['goalFollowUp']}, /n Name: {request_dict['name']}, /n age {request_dict['age']}, /n Description: {request_dict['descriptionsFollowUp']} /n from the previous text write in English 1description: write a long observation about description, 2Analysis of the description: write an analysis for the activity carried out, 3Evaluation: comparing the goal and observation, write and evaluate and tell me whether the goal was achieved or not. 4What is next: create a future activity related to the description",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'follow_up',
    }
    return  JsonResponse(new_dict)

def modify_critical_reflection_request(request):
   
    # Convertir el objeto JSON en un diccionario de Python
    request_dict = request.data

    variables = {
        'date': request_dict['date'],
        'description': request_dict['description']
    }
    # Crear un nuevo diccionario con los cambios deseados
    new_dict = {
        'message': f" date: {request_dict['date']}, I want you to act as a child care teacher using developmental milestones NQS and EYLF, PLANNING CYCLE, PRINCIPLES, PRACTICES and LEARNING OUTCOMES of the Early Years Learning Framework (EYLF). I will give you a daily reflections as an inputs an you will write 1.what worked well, 2.what to improve, 3.what action we should take. 4reflexion of everything. the reflections are: work well {request_dict['description']}",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'critical_reflection',
    }
    return  JsonResponse(new_dict)

def modify_weeklyReflection_request(request):
    # Convertir el objeto JSON en un diccionario de Python
    request_dict = request.data

    variables = {
        'date': request_dict['date'],
        'descriptions': request_dict['description_reflection'],
    }
    new_dict = {
        'message': f" date: {request_dict['date']},  want you to act as a child care teacher using developmental milestones NQS and EYLF, PLANNING CYCLE, PRINCIPLES, PRACTICES and LEARNING OUTCOMES of the Early Years Learning Framework (EYLF). I will give you a daily reflections as an inputs an you will write 1.what worked well, 2.what to improve, 3.what action we should take. 4reflexion of everything. the reflections are: {request_dict['description_reflection']}",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'weekly_reflection',
    }
    return  JsonResponse(new_dict)

def modify_weeklyPlanning_request(request):
    request_dict= request.data
    
    variables = {
        'date': request_dict['date'],
        'goals': request_dict['goals'],
        'range_age': request_dict['range_age']
        
    }
    
    new_dict = {
        'message': f" date: {request_dict['date']}, objective: {request_dict['goals']}/n 1.with the previous objective for a child of {request_dict['range_age']} years old write in English a title suitable to the objective 1.write the objective longer and professional, 2.EYLF Learning Outcomes suitable for the objective and how are them related, 3. EYLF principles suitable for the objective, 4.theorists suitable for the objective. 5.strategies suitable for the objective 6.activities suitable for the objective.  /n temperature=0.1",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'weeklyn_planning',
    
    }
    return JsonResponse(new_dict)

def create_cancellation_token():
    token_id = str(uuid.uuid4())
    cancellation_tokens[token_id] = asyncio.CancelToken()
    return token_id

def save_report(request):
    request_dict = request.data
    user = User.get_by_id(request_dict["token"])
    if user:
        user_id= request_dict['token']
        type_report= request_dict['typeReport'].lower().replace(" ", "_")
        report= request_dict['report']
        # Get the current timestamp
        timestamp = datetime.utcnow()
    
        if type_report in ['goal_report', 'follow_up', 'descriptions_report']:
            name = request_dict['childName']
            age = request_dict['age']
            child_id= request_dict['childId']
            child={
                "child_id": child_id,
                "child_name": name,
                "child_age": age,
            }
            save_report_data={
                "user_id": user_id,
                "type_report": type_report,
                "report": report,
                "child": child,
                "timestamp":timestamp
            }
            if type_report == 'descriptions_report':
                goalObservations = request_dict['goalObservations']
                save_report_data["goalObservations"] = goalObservations
            if type_report == 'follow_up':
                goalFollowUp = request_dict['goalFollowUp']
                save_report_data["goalFollowUp"] = goalFollowUp
   
        elif type_report == 'daily_report':
            rangeAgeDailyReport = request_dict['rangeAgeDailyReport']
            save_report_data={
                "user_id": user_id,
                "type_report": type_report,
                "report": report,
                "rangeAge": rangeAgeDailyReport,
                "timestamp":timestamp
            }
        elif type_report == 'weekly_planning':
            rangeAge = request_dict['rangeAge']
            save_report_data={
                "user_id": user_id,
                "type_report": 'weeklyn_planning',
                "report": report,
                "rangeAge": rangeAge,
                "timestamp":timestamp
            }
        else:
            save_report_data={
                "user_id": user_id,
                "type_report": type_report,
                "report": report,
                "timestamp":timestamp
            }
        save_report_id = HistoricalReportMongo.create(save_report_data).inserted_id
        

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)
    
def historical_reports(request):
    request_dict= request.data
    historical_report = HistoricalReportMongo.get_by_user_id(request_dict["token"])
      # Convert the cursor to a list of documents reports
    documents = [document for document in historical_report]
    json_documents = JSONEncoder().encode(documents)
    return JsonResponse(json.loads(json_documents), safe=False)

def historical_report(request):
    request_dict= request.data
    historical_report = HistoricalReportMongo.get_by_id(request_dict["token"])
      # Convert the cursor to a list of documents reports
    
    json_documents = JSONEncoder().encode(historical_report)
    return JsonResponse(json.loads(json_documents), safe=False)
    

def save_variables_report(request):
    request_dict = request
    user = User.get_by_id(request_dict["token"])
    if user:
        user_id= request_dict['token']
        type_report= request_dict['type_report']
        variables= request_dict['variables']
        response_chatgpt = request_dict['response_chatgpt']
        # Get the current timestamp
        timestamp = datetime.utcnow()
        
        save_report_data={
            "user_id": user_id,
            "type_report": type_report,
            "variables": variables,
            "response_chatgpt": response_chatgpt,
            "timestamp":timestamp
        }
        create_variables_reports = VariablesReport.create(save_report_data).inserted_id

def get_variables_reports(request):
    request_dict= request.data
    
    historical_variables_reports = VariablesReport.get_by_user_id(request_dict["token"])
      # Convert the cursor to a list of documents reports
    documents = [document for document in historical_variables_reports]
    json_documents = JSONEncoder().encode(documents)
    return JsonResponse(json.loads(json_documents), safe=False)


def modify_days_to_weekly_reflection(request):
    request_dict= request.data
    daily_reflections = []
  
    for document_id in request_dict['description']:
        daily_reflection = VariablesReport.get_by_id(document_id)
        daily_reflections.append(daily_reflection)
        
   
     # Concatenate descriptions of daily reflections
    descriptions = ', '.join([reflection['variables']['description'] for reflection in daily_reflections])
   
    variables = {
        'daily_reflections': descriptions
    }
    new_dict = {
        'message': f" I want you to act as a child care teacher using developmental milestones NQS and EYLF, PLANNING CYCLE, PRINCIPLES, PRACTICES and LEARNING OUTCOMES of the Early Years Learning Framework (EYLF). I will give you a daily reflections: {descriptions} with the previous reflections as an inputs  you will write: 1what worked well, 2what to improve, 3what action we should take. 4reflexion of everything.In english.",
        'variables': variables,
        'token': request_dict['token'],
        'type_report':'weekly_reflection',
    
    }
    
    return  JsonResponse(new_dict)

def modify_get_last_variable_report(request):
    request_dict= request.data
    last_variable_report = VariablesReport.get_last_doc(request_dict["token"],request_dict['typeReport'])
      # Convert the cursor to a list of documents reports
    json_documents = JSONEncoder().encode(last_variable_report)
    return JsonResponse(json.loads(json_documents), safe=False)

def modify_get_referral_link(request):
    token= request.data["token"]
    base_url = "http://localhost:3000/writewiseweb/referral-link/"
    referral_link = base_url + str(token)
    referral_code = token
    return JsonResponse({"referral_link": referral_link, "referral_code": referral_code})

   
def separar_items_reporte(reporte):
    # Dividir el reporte en secciones
    secciones = re.split(r'(\d+\..+?:)', reporte)
    # Eliminar cualquier espacio en blanco de la lista
    secciones = [s.strip() for s in secciones if s.strip()]
    # Crear un diccionario para almacenar las secciones
    reporte_dict = {}
    # Asumimos que las secciones impares son los títulos y las secciones pares son los contenidos
    for i in range(0, len(secciones), 2):
        titulo = re.sub(r'\d+\.\s+', '', secciones[i]).rstrip(':') 
        contenido = secciones[i+1]
        reporte_dict[titulo] = contenido

    return reporte_dict

def upload_to_drive(file_path):
    path_key_json = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'json', 'utopian-button-382400-f8559bf21161.json'))
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path_key_json, scope)
    gauth = GoogleAuth()
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({"title": os.path.basename(file_path)})    
    file.SetContentFile(file_path)
    file.Upload()

    # Get the shareable link of the uploaded file
    file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    return file['alternateLink']
    

def create_word(markers_list):
    path_file_word = os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'file', 'FormatoObservation.docx'))
    # Load the Word template
    doc = DocxTemplate(path_file_word)

    reports = []
    for markers in markers_list:
        data = f"Child: {markers['child_name']}   Date: {markers['date']}   Observer: {markers['childcareworker']}"
        last_report = markers == markers_list[-1]
        context = {'title': 'INDIVIDUAL OBSERVATION', 'data' : data, 'goal' : markers['goal'], 'description' : markers['description'],'analysis': markers['analysis'],'whatIsNext':markers['whatisnext'],'eylf': markers['eylf'], 'last': last_report }
        reports.append(context)

    doc.render({'reports': reports})

    # The file name of the document can be a constant or based on the current date/time
    name_file= f"{markers['child_name']}_individual_observation_{markers['date']}.docx"    
    path_to_save= os.path.abspath(os.path.join(settings.BASE_DIR, 'static', 'file', name_file))
    doc.save(path_to_save)
    
    file_link=upload_to_drive(path_to_save)
    # Delete the file after it has been uploaded
    try:
        os.remove(path_to_save)
        print(f"{path_to_save} has been removed successfully")
    except Exception as e:
        print(f"Error occurred while trying to remove {path_to_save}. Error message: {str(e)}")

    return file_link


def modify_create_word(request): 
    id_reports= request['selectedReports']
    markers_list = []
    for id in id_reports:
        get_report=HistoricalReportMongo.get_by_id(id)
        date= dateYYMMDD(get_report['timestamp'])
        get_user= User.get_by_id(get_report['user_id'])
        reporte_dict= separar_items_reporte(get_report['report'])
        # dictionary of keys (marker names) and values (new text)
        markers = {
        'child_name': get_report.get('child', {}).get('child_name', 'Default child name'),
        'childcareworker': get_user['username'],
        'date': date,
        'goal': get_report.get('goalObservations', 'default_value'),
        'analysis': reporte_dict.get('Analysis', 'default_value'),
        'description': reporte_dict.get('Description', 'default_value'),
        'eylf': reporte_dict.get('EYLF Learning Outcomes and sub-Outcomes suitable', 'default_value'),
        'whatisnext': reporte_dict.get('What is next') or reporte_dict.get("What's next", 'default_value'),
        }
        markers_list.append(markers)
    # Create the Word document
    link_doc= create_word(markers_list)
        
    return link_doc
    
   
    


