

from asyncio import StreamWriter
from calendar import c
from lib2to3.pgen2.token import OP
from queue import Queue
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List


app = FastAPI()


def search_id_found(user_id, _list): 
    return user_id in (list.id for list in _list)


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

#TODO:Filter getting nearby location using lat lng 
#TODO: Create function for searching
  
users: List[User] = []



@app.get("/api/v1/get-user-by-id/{user_id}")
def get_user_by_id(user_id: str):
       for index, item in enumerate(users): 
           if item.id == user_id: 
               return users[index]
          
       raise HTTPException(status_code=404, detail="User not found")

@app.get("/api/v1/get-users")
def get_users():    
    return users

@app.post("/api/v1/create-user")
def create_user(user: User):
    if search_id_found(user.id, users):
        raise HTTPException(status_code=409, detail="User already exist")

    users.append(user)
    return {"Success": "Successfully created User."}


@app.put("/api/v1/update-user/{item_id}")
def update_user(item_id:str, user:UpdateUser):

    for index,item in enumerate(users): 
        if item.id == item_id: 

            if user.name != None:
                users[index].name = user.name

            if user.address != None:
                users[index].address = user.address    

            if user.location != None:
                users[index].location = user.location    

            return {"Success":"Successfully updated User."}

       
    raise HTTPException(status_code=404, detail="User not found")

  

@app.delete("/api/v1/delete-user/{item_id}")
def delete_user(item_id:str = Query(..., description = "The id item to delete.")): 

    for item in users:
        if item.id == item_id: 
            users.remove(item)  
            return {"Success":"User Deleted!"}

    raise HTTPException(status_code=404, detail="User not found")















class Respondent(BaseModel):
    client_id:str

class RescueRequest(BaseModel):
    respondents:list[Respondent]
    
class UpdateRescueRequest(BaseModel):
    respondents:Optional[list[Respondent]] = None 

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
    rescueRequest:RescueRequest

class UpdateUserAssistance(BaseModel):
    confirmationDetails:Optional[ConfirmationDetail] = None    
    status:Optional[Status] = None    
    rescueRequest:Optional[RescueRequest] = None

users_assistance:List[UserAssistance] = []


@app.get("/api/v1/get-user-assistance-by-id/{user_id}")
def get_assistance_by_id(user_id: str):

    for index, item in enumerate(users_assistance): 
        if item.id == user_id:
            return users_assistance[index]

    raise HTTPException(status_code=404, detail="User Assistance not found!")
    
@app.get("/api/v1/get-users-assistance")
def get_assistance(): 
    return users_assistance

@app.post("/api/v1/create-user-assistance")
def create_user_assistance(assistance: UserAssistance):

    if search_id_found(assistance.id, users_assistance):
       raise HTTPException(status_code=409, detail="User Assistance already exists!") 

    users_assistance.append(assistance) 
    return {"Success":"Successfully created User Assistance."}  


@app.put("/api/v1/update-user-assistance/{item_id}")
def update_user_assistance(item_id: str, user: UpdateUserAssistance):
 
    for index, item in enumerate(users_assistance): 
        if item.id == item_id: 

             if user.confirmationDetails != None:
                  users_assistance[index].confirmationDetails = user.confirmationDetails     

             if user.status != None:
                  users_assistance[index].status = user.status 

             if user.rescueRequest != None:
                 users_assistance[index].rescueRequest = user.rescueRequest

             return {"Success":"Successfully Updated User Assistance"}    

    raise HTTPException(status_code=404, detail="User Assistance not found.")     


@app.delete("/api/v1/delete-user-assistance/{item_id}")
def delete_user_assistance(item_id:str = Query(..., description = "The id item to delete.")):

    for item in users_assistance: 
        if item.id == item_id: 
            users_assistance.remove(item)
            return {"Success":"User Assistance Deleted!"}

    raise HTTPException(status_code=404, detail="User Assistance not found.")
         














class HelpRequest(BaseModel):
    id:str
    client_id:str 
    accepted:bool

class UpdateHelpRequest(BaseModel):
     
    client_id:Optional[str] = None 
    accepted:Optional[bool] = None


help_requests: List[HelpRequest] = []



@app.get("/api/v1/get-help-request-by-id/{id},{client_id}")
def get_help_request_by_id(id:str, client_id:str): 
    for index, item in enumerate(help_requests):
        if item.id == id and item.client_id == client_id:
            return help_requests[index]

    raise HTTPException(status_code=404, detail="Help Request not found.")  


@app.post("/api/v1/create-help-request")
def create_help_request(request: HelpRequest):

    if search_id_found(request.id, help_requests):
        raise HTTPException(status_code=409, detail="Help Request already exists.")

    help_requests.append(request)
    return {"Success":"Successfully created Help Request."}

@app.put("/api/v1/update-help-request/{item_id}")
def update_help_request(item_id:str, request: UpdateHelpRequest):

    for index, item in enumerate(help_requests):
        if item.id == item_id:

            if request.client_id != None:
                help_requests[index].client_id = request.client_id

            if request.accepted != None:
                help_requests[index].accepted = request.accepted

            return {"Success":"Successfully Updated Help Request."}   
    
    raise HTTPException(status_code=404, detail="Help Request does not exist.")        

@app.delete("/api/v1/delete-help-request/{item_id}")
def delete_help_request(item_id:str = Query(..., description = "The help request item to delete.")):
 
    for item in help_requests:
        if item.id == item_id:
            help_requests.remove(item)
            return {"Success":"Help Request Deleted!"}

    raise HTTPException(status_code=404, detail="Help Request does not exist.")        







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



cancellation_events: List[Cancellation] = []

@app.get("/api/v1/get-cancellation-event/{id},{client_id}")
def get_cancellations(id:str, client_id:str):

    for index,item in enumerate(cancellation_events): 
        if item.id == id and item.client_id == client_id:
            return cancellation_events[index]

    raise HTTPException(status_code=404,detail="Cancellation Event not found.")

@app.post("/api/v1/create-cancellation-event")
def create_cancellation(cancellation: Cancellation):
    
    if search_id_found(cancellation.id, cancellation_events):
        raise HTTPException(status_code=409,detail="Cancellation Event already exist.")

    cancellation_events.append(cancellation)
    return {"Success":"Successfully created Cancellation Event."}


@app.put("/api/v1/update-cancellation-event/{item_id}")
def update_cancellation_reason(item_id:str, cancellation: UpdateCancellation):
    

    for index,item in enumerate(cancellation_events): 

        if item.id == item_id:

            if cancellation.client_id != None:
                cancellation_events[index].client_id = item.client_id

            if cancellation.cancellation_reason != None:
                cancellation_events[index].cancellation_reason = cancellation.cancellation_reason 

            return {"Success":"Successfully updated Cancellation Event"}

    raise HTTPException(status_code=404,detail="Cancellation Event not found.")
             



@app.delete("/api/v1/delete-cancellation-event/{item_id}")
def delete_rescue_request(item_id:str = Query(..., description = "The id item to delete.")):

    for item in cancellation_events: 
        if item.id == item_id:
            cancellation_events.remove(item)
            return {"Success":"Cancellation Event Deleted!"}

    raise HTTPException(status_code=404,detail="Cancellation Event does not exist.")