import json
from flask_restful import Resource
from flask import Response, request
from .tags_controller import (
    
    post_tags, 
    get_tag,
    delete_tags
    
)


class TagsApi(Resource):
    def post(self):
        body = request.get_json()
        rs = post_tags(body)
        rj = json.dumps(rs)
        return Response(rj, mimetype="application/json", status=rs['status'])
    
    def get(self):
        rs = get_tag()
        rj = json.dumps(rs)
        return Response(rj, mimetype="application/json", status=rs['status'])
    
    def delete(self):
        rs = delete_tags()
        rj = json.dumps(rs)
        return Response(rj, mimetype="application/json", status=rs['status'])