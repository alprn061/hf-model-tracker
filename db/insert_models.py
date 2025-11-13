from sqlalchemy import text
from loguru import logger
from typing import Dict, List
from db.test_connection import engine

def upsert_models(models: list[dict], tags_map: dict[str, list[str]], meta_map: dict[str, dict]):
    """
    Inserts/updates models, tags, and metadata.
    models: list of model_row dicts
    tags_map: { model_id: [tags] }
    meta_map: { model_id: {config, card_data} }
    """

    with engine.begin() as conn:
        # ---------------------------------------
        # 1) Upsert MODELS
        # ---------------------------------------
        model_query = text("""
                           INSERT INTO models (model_id, pipeline_tag, library_name, author, downloads, likes, last_modified, private)
                           VALUES (:model_id, :pipeline_tag, :library_name, :author, :downloads, :likes, :last_modified, :private)
                           ON CONFLICT (model_id)
                           DO UPDATE SET
                            pipeline_tag = EXCLUDED.pipeline_tag,
                            library_name = EXCLUDED.library_name,
                            author = EXCLUDED.author,
                            downloads = EXCLUDED.downloads,
                            likes = EXCLUDED.likes,
                            last_modified = EXCLUDED.last_modified,
                            private = EXCLUDED.private;
                           """)
        
        for model in models:
            conn.execute(model_query, model)
        logger.info(f"✅ Upserted {len(models)} model rows.")

        # ---------------------------------------
        # 2) Insert TAGS
        # ---------------------------------------
        tag_query = text("""
            INSERT INTO model_tags (model_id, tag)
            VALUES (:model_id, :tag)
            ON CONFLICT DO NOTHING;
        """)

        tag_count = 0
        for model_id, tags in tags_map.items():
            for tag in tags:
                conn.execute(tag_query, {"model_id": model_id, "tag": tag})
                tag_count += 1
        logger.info(f"🏷 Inserted {tag_count} tags.")

        # ---------------------------------------
        # 3) Upsert MODEL META
        # ---------------------------------------
        meta_query = text("""
                          INSERT INTO model_meta(model_id, config, card_data)
                          VALUES (:model_id, :config, :card_data)
                          ON CONFLICT (model_id)
                          DO UPDATE SET
                            config = EXCLUDED.config,
                            card_data = EXCLUDED.card_data;
                          """)
        for model_id, meta in meta_map.items():
            conn.execute(meta_query, {"model_id": model_id, "config": meta["config"], "card_data": meta["card_data"]})
        logger.info(f"📄 Upserted {len(meta_map)} meta rows.")
        return len(models), 0