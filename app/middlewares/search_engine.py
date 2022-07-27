import json
import requests

from app.extenstions import redis
from flask import current_app as app


def search_in_db(decorated_func):
    """
    a decorator that search a given content ID in database

    Args:
        decorated_func (_type_): decorated function
    """
    def search(**kwargs):
        app.logger.info(f"searching {kwargs.get('content_id')} in db")
        url = f"http://{app.config['CONTENT_MANAGER_HOST']}/content/{kwargs.get('content_id')}"
        response = requests.get(url)
        if response.status_code == 200:
            kwargs.update({"content_from_db": response.json().get("content")})
        return decorated_func(**kwargs)
    
    return search


def save_to_db(decorated_func):
    """
    a decorated that save a given content to database

    Args:
        decorated_func (_type_): decorated function
    """
    def save(**kwargs):
        if not "content_from_db" in kwargs:
            content, status_code = decorated_func(**kwargs)
            if status_code != 200:
                return content, status_code

            redis.lpush("new-content", json.dumps(content.json))
            return content, status_code
        return decorated_func(**kwargs)
    
    return save