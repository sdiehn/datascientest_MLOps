from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from typing import Optional
from fastapi import Header

class Item(BaseModel):
    itemid: int
    description: str
    owner: Optional[str] = None

api = FastAPI(
    title='My API'
)

@api.get('/headers')
def get_headers(user_agent=Header(None)):
    return {
        'User-Agent': user_agent
    }
@api.get('/')
def get_index(argument1):
    return {
        'data': argument1
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
@api.patch('/')
def patch_index():
    return {
        'method': 'patch',
        'endpoint': '/'
        }
