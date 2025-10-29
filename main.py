from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from typing import Optional
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime

data = [1, 2, 3, 4, 5]

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

class Item(BaseModel):
    itemid: int
    description: str
    owner: Optional[str] = None

class Computer(BaseModel):
    """a computer that is available in the store
    """
    computerid: int
    cpu: Optional[str]
    gpu: Optional[str]
    price: float

# api = FastAPI(
#     title="My API",
#     description="My own API powered by FastAPI.",
#     version="1.0.1")

responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}
@api.get('/thing', responses=responses)
def get_thing():
    return {
        'data': 'hello world'
    }

@api.get('/', tags=['home'])
def get_index():
    """returns greetings
    """
    return {
        'greetings': 'hello world'
    }

@api.get('/data')
def get_data(index):
    try:
        return {
            'data': data[int(index)]
        }
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )
@api.get('/items', tags=['home', 'items'])
def get_items():
    """returns an item
    """
    return {
        'item': "some item"
    }
@api.get('/custom', name='Get custom header')
def get_content(custom_header: Optional[str] = Header(None, description='My own personal header')):
    return {
        'Custom-Header': custom_header
    }

# @api.get('/', name="Hello World")
# def get_index():
#     """Returns greetings
#     """
#     return {'greetings': 'welcome'}

@api.get('/headers')
def get_headers(user_agent=Header(None)):
    return {
        'User-Agent': user_agent
    }

@api.get('/item/{itemid:float}')
def get_item_float(itemid):
    return {
        'route': 'dynamic',
        'itemid': itemid,
        'source': 'float'
    }
@api.get('/item/{itemid}')
def get_item_default(itemid):
    return {
        'route': 'dynamic',
        'itemid': itemid,
        'source': 'string'
    }


@api.get('/addition')
def get_addition(a: int, b: Optional[int]=None):
    if b:
        result = a + b
    else:
        result = a + 1
    return {
        'addition_result': result
    }

@api.get('/other')
def get_other():
    return {
        'method': 'get',
        'endpoint': '/other'
    }

@api.post('/item')
def post_item(item: Item):
    return {
        item
    }


@api.delete('/')
def delete_index():
    return {
        'method': 'delete',
        'endpoint': '/'
        }
@api.put('/')
def put_index():
    return {
        'method': 'put',
        'endpoint': '/'
        }

@api.put('/computer', name='Create a new computer')
def get_computer(computer: Computer):
    """Creates a new computer within the database
    """
    return computer
@api.patch('/')
def patch_index():
    return {
        'method': 'patch',
        'endpoint': '/'
        }
