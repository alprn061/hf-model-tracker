from pipeline.fetch_hf_models import fetch_models
from pipeline.normalize import normalize_model
from db.insert_models import upsert_models

data = fetch_models(limit=5)

models = []
tags_map = {}
meta_map = {}

for m in data:
    model_row, tags, meta = normalize_model(m)

    models.append(model_row)
    tags_map[model_row["model_id"]] = tags
    meta_map[model_row["model_id"]] = meta

upsert_models(models, tags_map, meta_map)