from fastapi import FastAPI
api = FastAPI()

api = FastAPI(
    title='User DB'
)

users_db = [
    {
        'user_id': 1,
        'name': 'Alice',
        'subscription': 'free tier'
    },
    {
        'user_id': 2,
        'name': 'Bob',
        'subscription': 'premium tier'
    },
    {
        'user_id': 3,
        'name': 'Clementine',
        'subscription': 'free tier'
    }
]


@api.get('/')
def get_index():
    return {'data': 'Welcome User'}

@api.get('/user')
def get_user_dict():
    return {
        users_db
    }

@api.get('/user/userid {user_id}')
def get_user_info(user_id: int ):
    for user in users_db:
        if user["user_id"] == user_id:
            return {
                'userid': user_id,
                'name': user['name'],
                'subscription': user['subscription'],
            }
    return []
   
@api.get('/user/userid/name {user_id}')
def get_user_info(user_id: int ):
    for user in users_db:
        if user["user_id"] == user_id:
            return {
                'name': user['name'],
            }
    return []
   
@api.get('/user/userid/subscription {user_id}')
def get_user_info(user_id: int ):
    for user in users_db:
        if user["user_id"] == user_id:
            return {
                'subscription': user['subscription'],
            }
    return []

@api.get('/other')
def get_other():
    return {
        'method': 'get',
        'endpoint': '/other'
    }
