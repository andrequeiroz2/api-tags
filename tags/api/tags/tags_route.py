from .tags_api import TagsApi

def init_tags_api(api):
    api.add_resource(TagsApi, "/api/users/tags")
