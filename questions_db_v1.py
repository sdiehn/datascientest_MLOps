from enum import Enum
import os
import pandas as pd
from fastapi import FastAPI, Query
from typing import List, Optional
from pydantic import BaseModel
from typing import Optional
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime

identifiers= {
    "admin": "4dm1N",
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    401: {"description": "Unauthorized"},
    400: {"description": "Bad Request"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

api = FastAPI(openapi_tags=[
    {
        'name': 'home',
        'description': 'default functions'
    },
    {
        'name': 'items',
        'description': 'functions that are used to deal with items'
    }
])

QUESTIONS_DF = pd.read_excel("questions_en.xlsx")

class UseEnum(str, Enum):
    positioning_test = "Positioning test"
    validation_test = "Validation test"
    total_boot_amp = "Total Boot Camp"

class SubjectEnum(str, Enum):
    databases = "Databases"
    distributed_systems = "Distributed systems"
    data_streaming = "Data Streaming"
    docker = "Docker"
    classification = "Classification"
    data_science = "data science"
    machine_learning = "machine-learning"
    automation = "Automation"

class MyException(Exception):
    def __init__(self,                 
                 name : str,
                 date: str):
        self.name = name
        self.date = date
@api.exception_handler(MyException)

def MyExceptionHandler(
    request: Request,
    exception: MyException
    ):
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own', 
            'date': exception.date
        }
    )
@api.get('/my_custom_exception')
def get_my_custom_exception():
    raise MyException(
      name='my error',
      date=str(datetime.datetime.now())
      )

def verify_credentials(auth_header: str):
    if not auth_header or not auth_header.startswith("Basic "):
        raise HTTPException(status_code=403, detail="Missing Authorization header")
    
    creds = auth_header.replace("Basic ", "").strip()
    try:
        username, password = creds.split(":")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid auth format")

    if username not in identifiers or identifiers[username] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return username


@api.get("/status")
def get_status():
    return {
        'status': 'ok'
    }

@api.get("/all_questions_list")
def list_questions():
    return {"questions": QUESTIONS_DF["question"].tolist()  }

@api.get("/questions_mcq")
def get_questions_mcq(
    request: Request,
    use: List[UseEnum]= Query(..., description="Use case to filter questions"),
    subject: List[SubjectEnum] = Query(..., description="Subjects to filter questions"),
    n: int = Query(5, description="Number of questions (5, 10, or 20)")
):

    auth_header = request.headers.get("Authorization")
    verify_credentials(auth_header)

    use_options = sorted(QUESTIONS_DF["use"].dropna().unique().tolist())
    subject_options = sorted(QUESTIONS_DF["subject"].dropna().unique().tolist())

    if not use and not subject:
        return {
            "use_options": use_options,
            "subject_options": subject_options,
            "message": "Select use and subject to generate questions"
        }

    filtered_questions = QUESTIONS_DF[
    (QUESTIONS_DF["use"] == use.value) &
    (QUESTIONS_DF["subject"].isin([subject.value]))
]
    if filtered_questions.empty:
        raise HTTPException(status_code=404, detail="No questions match the criteria")

    sample_size = min(n, len(filtered_questions))
    selected = filtered_questions.sample(sample_size)

    result = selected.to_dict(orient="records")
    return {"count": len(result), "questions": result}

@api.post("/questions")
async def create_question(request: Request):
    auth_header = request.headers.get("Authorization")
    username = verify_credentials(auth_header)

    if username != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create questions")

    data = await request.json()
    question = data.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing question text")

    QUESTIONS_DF.append(question)
    return {"message": "Question added", "question": question}


@api.get('/custom', name='Get custom header')
def get_content(custom_header: Optional[str] = Header(None, description='My own personal header')):
    return {
        'Custom-Header': custom_header
    }

@api.get('/headers')
def get_headers(user_agent=Header(None)):
    return {
        'User-Agent': user_agent
    }

@api.get('/other')
def get_other():
    return {
        'method': 'get',
        'endpoint': '/other'
    }
