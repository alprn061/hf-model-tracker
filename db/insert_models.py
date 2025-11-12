from sqlalchemy import text
from loguru import logger
from typing import Dict, List
from db.test_connection import engine

def upsert_models(models: List[Dict]):
    """
    Add new values Models table or update it
    """

    # 
    sql = text("""
        INSERT INTO models(
               model_id, pipeline_tag,library_name, author, downloads,
               likes, last_modified, private
               )
        VALUES(
               :model_id, :pipeline_tag, :library_name, :author, :downloads,
               :likes, :last_modified, :private)
        ON CONFLICT (model_id) DO UPDATE SET
               pipeline_tag = EXCLUDED.pipeline_tag,
               library_name = EXCLUDED.library_name,
               author = EXCLUDED.author,
               downloads = EXCLUDED.downloads,
               likes = EXCLUDED.likes,
               last_modified = EXCLUDED.last_modified,
               private = EXCLUDED.private
"""
    )
    inserted, updated = 0,0

    with engine.begin() as conn:
        for model in models:
            result = conn.execute(sql, model)

            inserted += 1
        logger.info(f"✅ Upserted {inserted} model rows into database.")