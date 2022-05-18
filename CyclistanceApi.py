

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



@app.get("/get-user-by-id/{user_id}")
def get_user_by_id(user_id: str):
       for index, item in enumerate(users): 
           if item.id == user_id: 
               return users[index]
          
       raise HTTPException(status_code=404, detail="User not found")

@app.get("/get-users")
def get_users():
    return users

@app.post("/create-user")
def create_user(user: User):
    if search_id_found(user.id, users):
        raise HTTPException(status_code=409, detail="User already exist")

    users.append(user)
    return {"Success": "Successfully created User."}


@app.put("/update-user/{item_id}")
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

        else: 
            raise HTTPException(status_code=404, detail="User not found")

  

@app.delete("/delete-user/{item_id}")
def delete_user(item_id:str = Query(..., description = "The id item to delete.")): 

    for item in users:
        if item.id == item_id: 
            users.remove(item)  
            return {"Success":"User Deleted!"}

    raise HTTPException(status_code=404, detail="User not found")
















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

users_assistance:List[UserAssistance] = []


@app.get("/get-user-assistance-by-id/{user_id}")
def get_assistance_by_id(user_id: str):

    for index, item in enumerate(users_assistance): 
        if item.id == user_id:
            return users_assistance[index]

    raise HTTPException(status_code=404, detail="User not found!")
    
@app.get("/get-users-assistance")
def get_assistance(): 
    return users_assistance

@app.post("/create-user-assistance")
def create_user_assistance(assistance: UserAssistance):

    if search_id_found(assistance.id, users_assistance):
       raise HTTPException(status_code=409, detail="User already exists!") 

    users_assistance.append(assistance) 
    return {"Success":"Successfully created User Assistance."}  


@app.put("/update-user-assistance/{item_id}")
def update_user_assistance(item_id: str, user: UpdateUserAssistance):
 
    for index, item in enumerate(users_assistance): 
        if item.id == item_id: 

             if user.confirmationDetails != None:
                  users_assistance[index].confirmationDetails = user.confirmationDetails     

             if user.status != None:
                  users_assistance[index].status = user.status 

             return {"Success":"Successfully Updated User Assistance"}    

        else: 
            raise HTTPException(status_code=404, detail="User not found.")     


@app.delete("/delete-user-assistance/{item_id}")
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


help_request: List[HelpRequest] = []

@app.get("/get-help-requests")
def get_help_requests(): 
    return help_request

@app.get("/get-help-request-by-id/{id},{client_id}")
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

@app.put("/update-help-request/{item_id}")
def update_help_request(item_id:str, request: UpdateHelpRequest):

    if item_id not in help_request:
        raise HTTPException(status_code=404, detail="Item does not exist.")

    if request.client_id != None:
        help_request[item_id].client_id = request.client_id

    if request.accepted != None:
        help_request[item_id].accepted = request.accepted    

    return help_request[item_id]        

@app.delete("delete-help-request/{item_id}")
def delete_help_request(item_id:str = Query(..., description = "The id item to delete.")):
    if item_id not in help_request:
        raise HTTPException(status_code=404, detail="Item does not exist.")

    del help_request[item_id]
    return {"Success":"Successfully Deleted."}    










 
    
class Respondent(BaseModel):
    client_id:str

class RescueRequest(BaseModel):
    id:str
    respondents:list[Respondent]
    
class UpdateRescueRequest(BaseModel):
    respondents:Optional[list[Respondent]] = None 

respondents = {}

@app.get("/get-rescue_request-by-id/{id}")
def get_rescue_request_by_id(id:str): 
    for item_id in respondents:
        if respondents[item_id].id == id:
            return respondents[item_id]
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/create-rescue-request")
def create_rescue_request(rescueRequest: RescueRequest):
    if rescueRequest.id in respondents:
        raise HTTPException(status_code=409, detail="Item already exists.")

    if rescueRequest.id in rescueRequest.respondents:
        raise HTTPException(status_code=409, detail="You can't be a respondent to your own request.")

    respondents[rescueRequest.id] = rescueRequest
    return respondents[rescueRequest.id]


@app.put("/update-rescue-request/{item_id}")
def update_rescue_request(item_id:str, rescueRequest: UpdateRescueRequest):
    
    if item_id not in respondents:
        raise HTTPException(status_code=404, detail="User not found.")

    if rescueRequest.respondents != None: 
        respondents[item_id].respondents = rescueRequest.respondents       

    return respondents[item_id]        

@app.delete("/delete-rescue-request/{item_id}")
def delete_rescue_request(item_id:str = Query(..., description = "The id item to delete.")):
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

@app.get("/get-cancellation-reason/{id},{client_id}")
def get_cancellations(id:str, client_id:str):
    for item_id in cancellations:
        if cancellations[item_id].id == id and cancellations[item_id].client_id == client_id:
            return cancellations[item_id]
    raise HTTPException(status_code=404,detail="User not found.")
    
@app.post("/create-cancellation-reason")
def create_cancellation(cancellation: Cancellation):
    if cancellation.id in cancellations:
        raise HTTPException(status_code=409,detail="Item already exist.")

    cancellations[cancellation.id] = cancellation    
    return cancellations[cancellation.id]
    
@app.put("/update-cancellation-reason/{item_id}")
def update_cancellation_reason(item_id:str, cancellation: UpdateCancellation):
    if item_id not in cancellations:
        raise HTTPException(status_code=404,detail="User not found.")

    if cancellation.client_id != None:
        cancellations[item_id].client_id = cancellation.client_id

    if cancellation.cancellation_reason != None:
        cancellations[item_id].cancellation_reason = cancellation.cancellation_reason

    return cancellations[item_id]        

@app.delete("/delete-cancellation-reason/{item_id}")
def delete_rescue_request(item_id:str = Query(..., description = "The id item to delete.")):
    if item_id not in cancellations:
        raise HTTPException(status_code=404,detail="Item does not exist.")

    del cancellations[item_id]
    return {"Success":"Successfully Deleted."}
