

from calendar import c
from lib2to3.pgen2.token import OP
from queue import Queue
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Location(BaseModel):
    lat: str
    lng: str


class User(BaseModel):
    id:str
    name:str
    address:str
    location:Location


class UpdateUser(BaseModel):
    name:Optional[str] = None
    address:Optional[str] = None
    location:Optional[Location] = None 

#Filter Date and time
#Filter getting nearby location using lat lng 


users = {}


@app.get("/get-user-by-id")
def get_user_by_id(user_id: str):
    for item_id in users: 
        if users[item_id].name == user_id: 
            return users[item_id]
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/get-users")
def get_users():
    return users

@app.post("/create-user")
def create_user(user: User):
    if user.id in users:
        raise HTTPException(status_code=409, detail="User already exist")
    users[user.id] = user
    return users[user.id]
        
@app.put("/update-user")
def update_user(item_id:str, user:UpdateUser):

    if item_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    if user.name != None:
        users[item_id].name = user.name

    if user.address != None:
        users[item_id].address = user.address    

    if user.location != None:
        users[item_id].location = user.location    

    return users[item_id]

@app.delete("/delete-user")
def delete_user(item_id:str = Query(..., description = "The id item to delete.")): 
    if item_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[item_id]
    return {"Success":"Item Deleted!"}

















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
    confirmationDetails: ConfirmationDetail
    status:Status

class UpdateUserAssistance(BaseModel):
    confirmationDetails:Optional[ConfirmationDetail] = None    
    status:Optional[Status] = None    

users_assistance = {}


@app.get("/get-user-assistance-by-id")
def get_assistance_by_id(user_id: str):
    for item_id in users:
        if users_assistance[item_id].id == user_id:
            return users_assistance[item_id]
    raise HTTPException(status_code=404, detail="User not found!")

@app.get("/get-user-assistance")
def get_assistance(): 
    return users_assistance

@app.post("/create-user-assistance")
def create_user_assistance(assistance: UserAssistance):
    if assistance.id in users_assistance:
        raise HTTPException(status_code=409, detail="User already exists!")
    users_assistance[assistance.id] = assistance
    return users_assistance[assistance.id]

@app.put("/update-user-assistance")
def update_user_assistance(item_id: str, user: UpdateUserAssistance):
    
    if item_id not in users_assistance:
        raise HTTPException(status_code=404, detail="User not found.")
 
    if user.confirmationDetails != None:
        users_assistance[item_id].confirmationDetails = user.confirmationDetails     

    if user.status != None:
        users_assistance[item_id].status = user.status

    return users_assistance[item_id]
    
@app.delete("/delete-user-assistance")
def delete_user_assistance(item_id:str = Query(..., description = "The id item to delete.")):
    if item_id not in users_assistance: 
        raise HTTPException(status_code=404, detail="User not found.")

    del users_assistance[item_id]  
    return {"Success":"Successfully Deleted!"} 









class HelpRequest(BaseModel):
    id:str
    client_id:str 
    accepted:bool

class UpdateHelpRequest(BaseModel):
     
    client_id:Optional[str] = None 
    accepted:Optional[bool] = None


help_request = {}

@app.get("/get-help-requests")
def get_help_requests(): 
    return help_request

@app.get("/get-help-request-by-id")
def get_help_request_by_id(id:str, client_id:str): 
    for item_id in help_request: 
        if help_request[item_id].id == id and help_request[item_id].client_id == client_id:
            return help_request[item_id]
    raise HTTPException(status_code=404, detail="User not found.")         

@app.post("/create-help-request")
def create_help_request(request: HelpRequest):
    if request.id in help_request:
        raise HTTPException(status_code=409, detail="Item ID already exists.")
    help_request[request.id] = request    
    return help_request[request.id]

@app.put("/update-help-request")
def update_help_request(item_id:str, request: UpdateHelpRequest):

    if item_id not in help_request:
        raise HTTPException(status_code=404, detail="Item does not exist.")

    if request.client_id != None:
        help_request[item_id].client_id = request.client_id

    if request.accepted != None:
        help_request[item_id].accepted = request.accepted    

    return help_request[item_id]        

@app.delete("delete-help-request")
def delete_help_request(item_id:str = Query(..., description = "The id item to delete.")):
    if item_id not in help_request:
        raise HTTPException(status_code=404, detail="Item does not exist.")

    del help_request[item_id]
    return {"Success":"Successfully Deleted."}    










 
    
class Respondent(BaseModel):
    id:str

class Response(BaseModel):
    id:str
    respondents:list[Respondent]
    
class UpdateResponse(BaseModel):
    respondents:Optional[list[Respondent]] = None 

respondents = {}

@app.get("/get-respondents-by-id")
def get_respondents_by_id(id:str): 
    for item_id in respondents:
        if respondents[item_id].id == id:
            return respondents[item_id]
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/create-response")
def create_respondent(response: Response):
    if response.id in respondents:
        raise HTTPException(status_code=409, detail="Item already exists.")

    if response.id in response.respondents:
        raise HTTPException(status_code=409, detail="You can't be a respondent to your own request.")

    respondents[response.id] = response
    return respondents[response.id]


@app.put("/update-response")
def update_respondent(item_id:str, response: UpdateResponse):
    
    if item_id not in respondents:
        raise HTTPException(status_code=404, detail="User not found.")

    if response.respondents != None: 
        respondents[item_id].respondents = response.respondents       

    return respondents[item_id]        

@app.delete("/delete-response")
def delete_response(item_id:str = Query(..., description = "The id item to delete.")):
    if item_id not in respondents:
        raise HTTPException(status_code=404, detail="User not found.")

    del respondents[item_id]
    return {"Success":"Successfully Deleted."}







class CancellationReason(BaseModel):
    reason:str
    message:str


class Cancellation(BaseModel):
    id:str
    client_id:str 
    cancellation_reason:list[CancellationReason]

class UpdateCancellation(BaseModel):
    client_id:Optional[str] = None
    cancellation_reason:Optional[list[CancellationReason]] = None



cancellations = {}

@app.get("/get-cancellation-reason")
def get_cancellations(id:str, clientId:str):
    for item_id in cancellations:
        if cancellations[item_id].id == id and cancellations[item_id].client_id == clientId:
            return cancellations[item_id]
    raise HTTPException(status_code=404,detail="User not found.")
    
@app.post("/create-cancellation-reason")
def create_cancellation(cancellation: Cancellation):
    if cancellation.id in cancellations:
        raise HTTPException(status_code=409,detail="Item already exist.")

    cancellations[cancellation.id] = cancellation    
    return cancellations[cancellation.id]
    
@app.put("/update-cancellation-reason")
def update_cancellation_reason(item_id:str, cancellation: UpdateCancellation):
    if item_id not in cancellations:
        raise HTTPException(status_code=404,detail="User not found.")

    if cancellation.client_id != None:
        cancellations[item_id].client_id = cancellation.client_id

    if cancellation.cancellation_reason != None:
        cancellations[item_id].cancellation_reason = cancellation.cancellation_reason

    return cancellations[item_id]        

@app.delete("/delete-cancellation-reason")
def delete_response(item_id:str = Query(..., description = "The id item to delete.")):
    if item_id not in cancellations:
        raise HTTPException(status_code=404,detail="Item does not exist.")

    del cancellations[item_id]
    return {"Success":"Successfully Deleted."}
# If returned result is already exist then edit the existing one
