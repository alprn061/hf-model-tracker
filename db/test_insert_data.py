from db.insert_models import upsert_models
from pipeline.normalize import normalize_model
from pipeline.fetch_hf_models import fetch_models

data = fetch_models(limit=3)
print("Fetched models:", len(data)) 
models = []

for m in data:
    model_row, tags, meta = normalize_model(m)
    models.append(model_row)

upsert_models(models)
