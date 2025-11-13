import time
from datetime import datetime, timezone
from loguru import logger

from pipeline.fetch_hf_models import fetch_models
from pipeline.normalize import normalize_model
from db.insert_models import upsert_models
from pipeline.snapshot import snapshot_models
from db.log_pipeline import log_pipeline_run


def run_pipeline(limit=20):

    start_time = datetime.now(timezone.utc)
    logger.info("🚀 Pipeline started")

    fetched_count = 0
    inserted_count = 0
    updated_count = 0
    error_count = 0

    try:
        # -------------------------------------------
        # 1) FETCH RAW DATA
        # -------------------------------------------
        raw_models = fetch_models(limit=limit)
        fetched_count = len(raw_models)
        logger.info(f"📥 Fetched {fetched_count} models from HF API")

        # -------------------------------------------
        # 2) NORMALIZE
        # -------------------------------------------
        normalized = []
        for model in raw_models:
            try:
                m_row, tags, meta = normalize_model(model)
                normalized.append((m_row, tags, meta))
            except Exception as e:
                model_id = model["id"] if isinstance(model, dict) else str(model)
                logger.error(f"❌ Normalize error for {model_id}: {e}")
                error_count += 1

        # -------------------------------------------
        # 3) UPSERT INTO DATABASE
        # -------------------------------------------
        model_rows = {}
        tags_map = {}
        meta_map = {}

        for (m_row, tags, meta) in normalized:
            model_id = m_row["model_id"]
            model_rows[model_id] = m_row
            tags_map[model_id] = tags
            meta_map[model_id] = meta

        inserted_count, updated_count = upsert_models(
            list(model_rows.values()),
            tags_map,
            meta_map
        )

        # -------------------------------------------
        # 4) SNAPSHOT TODAY
        # -------------------------------------------
        snapshot_models(list(model_rows.values()))   # ← DOĞRU OLAN BU

        logger.success("🎉 Pipeline executed successfully!")
        status_message = "success"

    except Exception as e:
        logger.error(f"💥 PIPELINE FAILED: {e}")
        error_count += 1
        status_message = f"failed: {e}"

    # -------------------------------------------
    # 5) LOG PIPELINE RUN
    # -------------------------------------------
    end_time = datetime.now(timezone.utc)

    log_pipeline_run(
        start_time=start_time,
        end_time=end_time,
        fetched_count=fetched_count,
        inserted_count=inserted_count,
        updated_count=updated_count,
        error_count=error_count,
        message=status_message
    )

    logger.info("📌 Pipeline log written to database.")


if __name__ == "__main__":
    run_pipeline(limit=20)
