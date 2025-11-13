from sqlalchemy import text
from db.test_connection import engine
from loguru import logger
from datetime import date


def snapshot_models(models: list[dict]):
    """
    Inserts today's downloads & likes into model_snapshots table.
    Avoids duplicates for the same model on the same day.
    """
    
    if not models:
        logger.warning("⚠ No models provided to snapshot.")
        return
    
    today = date.today()

    rows = [
        (m["model_id"], m["downloads"], m["likes"])
        for m in models
        if m.get("model_id")
    ]

    if not rows:
        logger.warning("⚠ No valid rows to snapshot.")
        return
    
    insert_query = text("""
                        INSERT INTO model_snapshots (model_id, downloads, likes, snapshot_date)
                        VALUES (:model_id, :downloads, :likes, :snapshot_date)
                        ON CONFLICT (model_id, snapshot_date) DO NOTHING;
                        """)
    inserted_count = 0

    with engine.begin() as conn:
       for r in rows:
          conn.execute(insert_query, {
            "model_id": r[0],
            "downloads": r[1],
            "likes": r[2],
            "snapshot_date": today
          })
          inserted_count += 1
    logger.info(f"📸 Inserted {inserted_count} snapshot rows for date {today}.")