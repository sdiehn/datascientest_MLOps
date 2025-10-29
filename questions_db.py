from enum import Enum
import pandas as pd
from fastapi import FastAPI, Header, Query, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi import Request
import datetime
import os


identifiers = {
    "admin": "4dm1N",
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

security = HTTPBasic()

def verify_credentials_httpbasic(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    if username not in identifiers or identifiers[username] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return username

api = FastAPI(title="Question API", openapi_tags=[
    {
        'name': 'home',
        'description': 'default functions'
    },
    {
        'name': 'items',
        'description': 'functions that are used to deal with items'
    }
])  

QUESTIONS_PATH = "questions_en.xlsx"
QUESTIONS_DF = pd.read_excel(QUESTIONS_PATH)    

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
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date

@api.exception_handler(MyException)
def MyExceptionHandler(request: Request, exception: MyException):
    return JSONResponse(
        status_code=418,
        content={
            "url": str(request.url),
            "name": exception.name,
            "message": "This error is my own",
            "date": exception.date
        }
    )

@api.get('/my_custom_exception')
def get_my_custom_exception():
    raise MyException(
        name='my error',
        date=str(datetime.datetime.now())
    )

@api.get("/status")
def get_status():
    return {"status": "ok"}


@api.get("/questions")
def get_questions():
    return {"questions": QUESTIONS_DF["question"].tolist()}

@api.get("/questions_mcq")
def get_questions_mcq(
    use: UseEnum = Query(..., description="the type of MCQ for which this question is used"),
    subject: SubjectEnum = Query(..., description="the category of the question"),
    n: int = Query(5, description="Number of questions (5, 10, or 20)")
):
    try:
        if n not in [5, 10, 20]:
            raise HTTPException(status_code=400, detail="n must be 5, 10, or 20")
        
        QUESTIONS_DF["use_clean"] = QUESTIONS_DF["use"].astype(str).str.strip().str.lower()
        QUESTIONS_DF["subject_clean"] = QUESTIONS_DF["subject"].astype(str).str.strip().str.lower()
        
        filtered_questions = QUESTIONS_DF[
            (QUESTIONS_DF["use_clean"] == use.value.lower()) &
            (QUESTIONS_DF["subject_clean"] == subject.value.lower())
        ]

        if filtered_questions.empty:
            raise HTTPException(status_code=404, detail="No questions match the criteria")

        sample_size = min(n, len(filtered_questions))
        selected = filtered_questions.sample(n=sample_size, replace=False)

        return {
            "questions": selected.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@api.post("/questions")
async def create_question(request: Request, username: str = Depends(verify_credentials_httpbasic)):
    if username != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create questions")

    data = await request.json()
    required_fields = ["question", "subject",  "use", "correct","responseA", "responseB", "responseC", "responseD" ]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
        
    global QUESTIONS_DF
    new_row = pd.DataFrame([data])
    QUESTIONS_DF = pd.concat([QUESTIONS_DF, new_row], ignore_index=True)
    QUESTIONS_DF.to_excel(QUESTIONS_PATH, index=False)

    return {"message": "Question added to Excel", "question": data["question"]}


@api.get('/custom', name='Get custom header')
def get_content(custom_header: Optional[str] = Header(None, description='My own personal header')):
    return {"Custom-Header": custom_header}

@api.get('/headers')
def get_headers(user_agent=Header(None)):
    return {"User-Agent": user_agent}

@api.get('/other')
def get_other():
    return {"method": 'get', "endpoint": '/other'}
