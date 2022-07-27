import requests

from typing import Any, Dict, Tuple
from flask import jsonify
from flask import current_app as app
from app.utils.errors import Errors as err
from app.middlewares import search_engine as search_engine_middlewares


# TODO do logs


class SearchEngine:

    def autocomplete(prefix: str) -> Tuple[Dict, int]:
        url = f"https://{app.config['RAPID_API_AUTOCOMPLETE_HOST']}/auto-complete"

        headers = {
            "X-RapidAPI-Host": app.config["RAPID_API_AUTOCOMPLETE_HOST"],
            "X-RapidAPI-Key": app.config["RAPID_API_KEY"]
        }

        response = requests.get(url, headers=headers, params={"q": prefix})
        if response.status_code != 200:
            return err.rapid_api_error(response.status_code, response.text)

        autocomplete_results = [{
            "content-name": result["l"],
            "content-id": result["id"]
            } for result in response.json()["d"]]

        return jsonify(results=autocomplete_results), 200


    @search_engine_middlewares.search_in_db
    @search_engine_middlewares.save_to_db
    def get_content_by_id(**kwargs: Dict[str, Any]) -> Tuple[Dict, int]:
        if "content_from_db" in kwargs:
            return jsonify(kwargs.get("content_from_db")), 200
        
        url = f"https://{app.config['RAPID_API_CONTENT_DATA_HOST']}/imdb_api/movie"

        headers = {
            "X-RapidAPI-Host": app.config["RAPID_API_CONTENT_DATA_HOST"],
            "X-RapidAPI-Key": app.config["RAPID_API_KEY"]
        }

        response = requests.get(url, headers=headers, params={"id": kwargs.get("content_id")})
        if response.status_code != 200:
            return err.rapid_api_error(response.status_code, response.text)

        return jsonify(response.json()), 200