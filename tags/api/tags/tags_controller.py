from flask import request
from .tags_model import Tags
from firebase_admin import auth
from functools import wraps
from .validation import valid_tag
from mongoengine.errors import DoesNotExist
from tags import firebase


def valid_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {"msg":"error","inf": "No token provided", "status": 400}
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {"msg":"error","inf":"Invalid token provided", "status": 400}
        return f(*args, **kwargs)
    return wrap


@valid_token
def post_tags(body):
    tag = body['tag']
    valid = valid_tag(tag)
    if "error" in valid.keys():
        resp = {
            "msg": "error",
            "inf": valid['error'],
            "status": 400
        }
        return resp

    token = request.headers['authorization']
    decoded_token = auth.verify_id_token(token)
    email = decoded_token['firebase']['identities']['email'][0]
    
    try:
        Tags.objects(email=email)
        Tags.objects(email=email).update_one(push__tags=tag)
        x  = Tags.objects.get(email=email)
        resp = {
            "msg":"success",
            "data":[{
                "email": x["email"],
                "tags": x["tags"]
            }], 
            "status": 200
        }
        return resp
    except DoesNotExist:
        Tags(email=email).save()
        Tags.objects(email=email).update_one(push__tags=tag)

        x  = Tags.objects.get(email=email)

        resp = {
            "msg":"success",
            "data":[{
                "email": x["email"],
                "tags": x["tags"]
            }], 
            "status": 200
        }
        return resp


@valid_token
def get_tag():
    token = request.headers['authorization']
    decoded_token = auth.verify_id_token(token)
    email = decoded_token['firebase']['identities']['email'][0]
    
    try:
        tag = Tags.objects.get(email=email)
        resp = {
            "msg":"success",
            "data":[{
                "tags": tag['tags']
            }], 
            "status": 200
        }
        return resp
    except DoesNotExist:
        resp = {
            "msg":"error",
            "data":[{
                "tags": "Tags not found"
            }], 
            "status": 400
        }
        return resp


@valid_token
def delete_tags():
    token = request.headers['authorization']
    decoded_token = auth.verify_id_token(token)
    email = decoded_token['firebase']['identities']['email'][0]
    try:
        tag = Tags.objects.get(email=email)
        Tags.objects(email=email).delete()
        resp = {
            "msg":"success",
            "inf":"Tags deleted", 
            "status": 200
        }
        return resp

    except DoesNotExist:
        resp = {
            "msg":"error",
            "data":[{
                "tags": "Tags not found"
            }], 
            "status": 400
        }
        return resp
