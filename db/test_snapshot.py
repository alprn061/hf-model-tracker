from pipeline.fetch_hf_models import fetch_models
from pipeline.normalize import normalize_model
from db.insert_models import upsert_models
from pipeline.snapshot import snapshot_models


#  fetch models
models_raw = fetch_models(limit=5)

# Normalize
model_rows = []
tags = []
metas = []

for m in models_raw:
    model_row, model_tags, meta_row = normalize_model(m)
    model_rows.append(model_row)
    tags.append((model_row["model_id"], model_tags))
    metas.append(meta_row)

# Insert/Upsert models into DB
upsert_models(model_rows)

# Snapshot after models exist
snapshot_models(model_rows)
