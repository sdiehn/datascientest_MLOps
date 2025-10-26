from fastapi import FastAPI
api = FastAPI()
@api.get('/')
def get_index():
    return {
        'method': 'get',
        'endpoint': '/'
        }
@api.get('/other')
def get_other():
    return {
        'method': 'get',
        'endpoint': '/other'
    }
@api.post('/')
def post_index():
    return {
        'method': 'post',
        'endpoint': '/'
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
