from fastapi import APIRouter, HTTPException, Form
from backend.app.routers.dataset_router import STORED_DATASETS, ACTIVE_DATASET_ID
from backend.app.services.ml_engine import GLOBAL_ML_ENGINE

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

@router.post("/train")
async def train_model():
    if not ACTIVE_DATASET_ID or ACTIVE_DATASET_ID not in STORED_DATASETS:
        raise HTTPException(status_code=404, detail="No active dataset loaded.")
        
    ds = STORED_DATASETS[ACTIVE_DATASET_ID]
    pdf = ds["processed_df"]
    
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=400, detail="Processed dataset is empty.")
        
    try:
        results = GLOBAL_ML_ENGINE.train_model(pdf, text_col='Cleaned_Text', label_col='Label')
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict")
async def predict_review(text: str = Form(...)):
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty.")
    res = GLOBAL_ML_ENGINE.predict_sentiment(text)
    return {"status": "success", "prediction": res}
