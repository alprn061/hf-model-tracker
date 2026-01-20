"""
MODULE: Database Schemas (ORM Mapping)
DESCRIPTION: 
    Pydantic models representing the Supabase (PostgreSQL) database structure.
    Used for data validation, serialization, and type safety across the pipeline.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from typing import Optional
from uuid import UUID

# --- Base Config for ORM Compatibility ---
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# ---------------------------------------------------------
# 1. TABLE: public.models
# ---------------------------------------------------------
class HFModel(BaseSchema):
    """
    Core registry of Hugging Face models.
    Reflects the current state of the model metadata.
    """
    model_id: str = Field(..., description="Unique HF model identifier (e.g. 'meta-llama/Llama-2-7b')")
    pipeline_tag: Optional[str] = Field(None, description="NLP/CV task (e.g. 'text-generation')")
    library_name: Optional[str] = Field(None, description="Framework (e.g. 'transformers', 'diffusers')")
    author: Optional[str] = Field(None, description="Organization or user account")
    
    # Metrics
    downloads: int = Field(0, description="Rolling monthly downloads (Last 30 Days)")
    likes: int = Field(0, description="Total all-time likes")
    
    # Flags & Timestamps
    private: bool = False
    is_active: bool = True
    last_modified: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)

# ---------------------------------------------------------
# 2. TABLE: public.model_tags
# ---------------------------------------------------------
class ModelTag(BaseSchema):
    """
    Normalized tags for filtering (One-to-Many relationship with models).
    """
    id: int
    model_id: str
    tag: str = Field(..., description="Specific tag (e.g. 'autotrain_compatible', 'license:mit')")

# ---------------------------------------------------------
# 3. TABLE: public.model_snapshots
# ---------------------------------------------------------
class ModelSnapshot(BaseSchema):
    """
    Daily historical data points used to calculate velocity and trends.
    """
    id: int
    model_id: str
    snapshot_date: date
    pipeline_tag: Optional[str]
    
    downloads: int = Field(..., description="Download count (30-day rolling) at snapshot time")
    likes: int = Field(..., description="Like count at snapshot time")
    is_active: bool = True

# ---------------------------------------------------------
# 4. TABLE: public.daily_trends (THE PREDICTION ENGINE OUTPUT)
# ---------------------------------------------------------
class DailyTrend(BaseSchema):
    """
    Output table for the Machine Learning Pipeline.
    Stores the probability scores and calculated momentum metrics.
    """
    id: int
    model_id: str
    
    # ML Outputs
    probability: float = Field(..., description="XGBoost predicted trend probability (0.0 - 1.0)")
    prediction_date: date
    
    # Momentum Features
    growth_yesterday: float = Field(..., description="Calculated velocity (Growth %)")
    downloads_yesterday: int = Field(..., description="Absolute volume change (Delta) from previous day")
    
    created_at: datetime

# ---------------------------------------------------------
# 5. TABLE: public.pipeline_log
# ---------------------------------------------------------
class PipelineLog(BaseSchema):
    """
    Audit trail for ETL and ML jobs (Observability).
    """
    run_id: UUID = Field(..., description="Unique execution ID")
    created_at: datetime
    
    # Timing
    start_time: datetime
    end_time: Optional[datetime] = None
    
    # Statistics
    fetched_count: int = 0
    inserted_count: int = 0
    updated_count: int = 0
    error_count: int = 0
    
    log_message: Optional[str] = Field("success", description="Status or error details")