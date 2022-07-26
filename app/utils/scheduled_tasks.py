import json
import requests

from app.extenstions import scheduler, redis
from flask import current_app as app


@scheduler.task(trigger="interval", id="pop_messages_from_redis", seconds=10, max_instances=1)
def pop_messages_from_redis():
    with scheduler.app.app_context():
        content = redis.rpop("new-content")
        if not content:
            return

        url = f"http://{scheduler.app.config['CONTENT_MANAGER_HOST']}/content"
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=json.loads(content))
        if response.status_code != 201:
            app.logger.info(f"error during saving content {json.loads(content).get('id')}. the content returned to the queue")
            redis.lpush("new-content", content)
            return

        app.logger.info(response.json().get("msg"))