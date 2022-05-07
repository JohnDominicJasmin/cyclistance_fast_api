from ast import Str
from audioop import add
from datetime import date

from fastapi import FastAPI, Path
from pydantic import BaseModel



app = FastAPI()

class Location(BaseModel):
    lat: str
    lng: str


class User(BaseModel):
    id:str
    name:str
    address:str
    location:Location

#Filter Date and time

users = {}


@app.get("/get-user-by-id")
def get_user_by_id(user_id: str):
    for item_id in users: 
        if users[item_id].name == user_id: 
            return users[item_id]
    return {"Data" : "Not Found"}        

@app.get("/get-users")
def get_users():
    return users

@app.post("/create-user")
def create_user(user: User):
    if user.id in users:
        return {"Error": "Item ID already exists."}
    users[user.id] = user
    return users[user.id]
        
#Add post and put method


















class ConfirmationDetail(BaseModel):
    address:str
    bike_type:str
    description:str
    message:str

class Status(BaseModel):
    searching:bool
    started:bool
    ongoing:bool
    finished:bool

class UserAssistance(BaseModel):
    id:str
    date:str
    confirmationDetails: ConfirmationDetail
    status:Status

users_assistance = {}


@app.get("/get-assistance-by-id")
def get_assistance_by_id(user_id: str):
    for item_id in users:
        if users_assistance[item_id].id == user_id:
            return users_assistance[item_id]
    return {"Data" : "Not Found"}        

@app.get("/get-assistance")
def get_assistance(): 
    return users_assistance

@app.post("/create-user-assistance")
def create_user_assistance(assistance: UserAssistance):
    if assistance.id in users_assistance:
        return {"Error": "Item ID already exists."}
    users_assistance[assistance.id] = assistance
    return users_assistance[assistance.id]

#Add post and put method





class HelpRequest(BaseModel):
    id:str
    client_id:str 
    date:str 
    accepted:bool



help_request = {}

@app.get("/get-help-requests")
def get_help_requests(): 
    return help_request

@app.get("/get-help-request-by-id")
def get_help_request_by_id(id:str, client_id:str): 
    for item_id in help_request: 
        if help_request[item_id].id == id and help_request[item_id].client_id == client_id:
            return help_request[item_id]
    return { "Data":"Not Found" }        

@app.post("/create-help-request")
def create_help_request(request: HelpRequest):
    if request.id in help_request:
        return {"Error": "Item ID already exists."}
    help_request[request.id] = request    
    return help_request[request.id]

#Add post and put method







 
    
class Respondent(BaseModel):
    id:str

class Responce(BaseModel):
    id:str
    date:str
    respondents:list[Respondent]
    


respondents = {}

@app.get("/get-respondents-by-id")
def get_respondents_by_id(id:str): 
    for item_id in respondents:
        if respondents[item_id].id == id:
            return respondents[item_id]
    return {"Data":"Not Found"}        

@app.post("/create-responce")
def create_respondent(responce: Responce):
    if responce.id in respondents:
        return {"Error": "Responce Id Already Exist."} 

    if responce.id in responce.respondents:
        return {"Error":"You can't be a respondent to your own request."}

    respondents[responce.id] = responce
    return respondents[responce.id]


#Add post and put method













class CancellationReason(BaseModel):
    reason:str
    message:str


class Cancellation(BaseModel):
    id:str
    client_id:str 
    cancellation_reason:list[CancellationReason]



cancellations = {}

@app.get("/get-cancellation-reason  ")
def get_cancellations(id:str, clientId:str):
    for item_id in cancellations:
        if cancellations[item_id].id == id and cancellations[item_id].client_id == clientId:
            return cancellations[item_id]
    return {"Data":"Not Found"}        
    
@app.post("/create-cancellation")
def create_cancellation(cancellation: Cancellation):
    if cancellation.id in cancellations:
        return {"Error": "Id Already Exist."} 

    cancellations[cancellation.id] = cancellation    
    return cancellations[cancellation.id]
    


# If returned result is already exist then edit the existing one
