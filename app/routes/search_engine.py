from typing import Dict, Tuple
from flask import Blueprint
from app.services.search_engine import SearchEngine


search_engine_bp = Blueprint("search_engine_bp", __name__)


@search_engine_bp.get("/autocomplete/<string:prefix>")
def search_engine_autocomplete(prefix: str) -> Tuple[Dict, int]:
    return SearchEngine.autocomplete(prefix)


@search_engine_bp.get("/content/<string:id>")
def get_content_by_id(id: str) -> Tuple[Dict, int]:
    return SearchEngine.get_content_by_id(content_id=id)