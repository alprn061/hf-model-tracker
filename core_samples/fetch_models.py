"""
MODULE: Hugging Face Data Ingestion (Demo)
AUTHOR: Alperen Aydın
DESCRIPTION:
    This module handles the extraction of model metadata from the Hugging Face API.
    It employs a multi-phase fetching strategy to ensure a diverse dataset:
    
    - Phase 1: Top Downloads (Global Popularity)
    - Phase 2: Top Likes (Community Favorites)
    - Phase 3: Trending (7-day Velocity)
    - Phase 4: Fresh Models (Recently Created)
    - Phase 5: Targeted Fetch (Specific Pipeline x Library combinations)
    
    NOTE: This is a simplified version of the production ETL script for demonstration.
"""

import os
import requests
from typing import List, Dict, Optional
from loguru import logger
from dotenv import load_dotenv

# Load environment variables (API Keys)
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
BASE_URL = "https://huggingface.co/api/models"

class ModelFetcher:
    """
    Handles robust data fetching from Hugging Face with pagination and error handling.
    """
    
    def __init__(self, timeout: int = 45):
        self.timeout = timeout
        self.headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

    def fetch_global_top_models(self, limit: int = 1000, sort_by: str = "downloads") -> List[Dict]:
        """
        Fetches top models globally without category restrictions.
        
        Args:
            limit (int): Number of models to fetch.
            sort_by (str): Metric to sort by (downloads, likes, likes7d, createdAt).
            
        Returns:
            List[Dict]: List of model metadata dictionaries.
        """
        logger.info(f"🌍 Global Fetch Initiated: Top {limit} by '{sort_by}'")
        
        params = {
            "limit": limit,
            "sort": sort_by,
            "direction": -1,  # Descending
            "full": True      # Fetch full metadata
        }

        try:
            response = requests.get(
                BASE_URL, 
                params=params, 
                headers=self.headers, 
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list):
                logger.success(f"✅ Extracted {len(data)} models (Sort: {sort_by})")
                return data
            return []

        except requests.exceptions.Timeout:
            logger.error(f"⏳ Timeout during global fetch ({sort_by})")
            return []
        except Exception as e:
            logger.error(f"❌ Global fetch failed: {e}")
            return []

    def fetch_category_specific(self, pipeline_tag: str, library: str, limit: int = 200) -> List[Dict]:
        """
        Fetches models for a specific Pipeline x Library combination (e.g., 'text-generation' x 'pytorch').
        """
        params = {
            "pipeline_tag": pipeline_tag,
            "library": library,
            "limit": limit,
            "sort": "downloads",
        }

        try:
            response = requests.get(
                BASE_URL, 
                params=params, 
                headers=self.headers, 
                timeout=25
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.warning(f"⚠ Failed to fetch {pipeline_tag} x {library}: {e}")
            return []

    def run_etl_pipeline(self):
        """
        Executes the full multi-phase data ingestion strategy.
        """
        unique_models = {}

        # --- Phase 1: Global Popularity ---
        logger.info("📡 Phase 1: Fetching Top Downloads...")
        for model in self.fetch_global_top_models(limit=1000, sort_by="downloads"):
            unique_models[model.get("id")] = model

        # --- Phase 2: Community Favorites ---
        logger.info("❤️ Phase 2: Fetching Top Likes...")
        for model in self.fetch_global_top_models(limit=1000, sort_by="likes"):
            unique_models[model.get("id")] = model

        # --- Phase 3: Trending Momentum ---
        logger.info("🚀 Phase 3: Fetching Trending (7d Velocity)...")
        for model in self.fetch_global_top_models(limit=1000, sort_by="likes7d"):
            unique_models[model.get("id")] = model
            
        # --- Phase 4: Fresh Content ---
        logger.info("🆕 Phase 4: Fetching Recently Created...")
        for model in self.fetch_global_top_models(limit=100, sort_by="createdAt"):
            unique_models[model.get("id")] = model

        logger.success(f"🎉 ETL Complete. Total Unique Models Ingested: {len(unique_models)}")
        return list(unique_models.values())

if __name__ == "__main__":
    # Demo execution
    fetcher = ModelFetcher()
    data = fetcher.run_etl_pipeline()
    print(f"Sample Data Point: {data[0]['id'] if data else 'No Data'}")