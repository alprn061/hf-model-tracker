from sqlalchemy import text
from db.test_connection import engine
from datetime import datetime

def log_pipeline_run(
    start_time,
    end_time,
    fetched_count,
    inserted_count,
    updated_count,
    error_count,
    message="OK"
):
    sql = text("""
        INSERT INTO pipeline_log (
            start_time, end_time, fetched_count, inserted_count,
            updated_count, error_count, log_message
        )
        VALUES (
            :start_time, :end_time, :fetched_count, :inserted_count,
            :updated_count, :error_count, :log_message
        );
    """)

    with engine.begin() as conn:
        conn.execute(sql, {
            "start_time": start_time,
            "end_time": end_time,
            "fetched_count": fetched_count,
            "inserted_count": inserted_count,
            "updated_count": updated_count,
            "error_count": error_count,
            "log_message": message
        })