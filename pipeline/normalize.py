from typing import Dict, Any, List, Tuple
from datetime import datetime

def parse_ts(iso_str: str | None) -> datetime | None:
    """ Convert ISO 8601 to Datetime object"""
    if not iso_str:
        return None
    try:
        # HuggingFace's datetime format is 2025-11-04T08:25:31.000Z
        # convert "Z" to "UTC"
        if iso_str.endswith("Z"):
            iso_str = iso_str.replace("Z", "+00:00")
        return datetime.fromisoformat(iso_str)
    except Exception:
        return None

def normalize_model(m: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str], Dict[str, Any]]:
    """ Normalize a HF Model object"""
    # -------- MODELS TABLE --------
    # MODELS : "id"="moonshotai/Kimi-K2-Thinking",...
    model_id = m.get("id")
    author = model_id.split("/")[0] if model_id and "/" in model_id else None

    model_row = {
        "model_id" : model_id,
        "pipeline_tag": m.get("pipeline_tag"),
        "library_name" : m.get("library_name"),
        "author" : author,
        "downloads": m.get("downloads"),
        "likes" : m.get("likes"),
        "last_modified" : parse_ts(m.get("createdAt") or m.get("lastModified")),
        "private": bool(m.get("private", False))
    }

    # -------- TAGS TABLE --------
    # TAGS: tags=[transformers,...] "
    tags = m.get("tags") or []
    tags = [t for t in tags if isinstance(t, str)] # keep only string tags

    # -------- META TABLE --------
    # META: config ="", card_data=""
    meta_row ={
            "model_id" : model_id,
            "config" : m.get("config"),
        "card_data" : m.get("cardData") #only full=true
    }

    return model_row, tags, meta_row

