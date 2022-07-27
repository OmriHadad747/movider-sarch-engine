from typing import Dict, Tuple
from flask import jsonify


class Errors:

    @classmethod
    def rapid_api_error(cls, status_code: int, err_msg: str) -> Tuple[Dict, int]:
        return jsonify(err_msg=f"error from rapid api: {err_msg}"), status_code