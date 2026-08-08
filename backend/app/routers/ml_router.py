from fastapi import APIRouter, HTTPException, Request
import backend.app.routers.dataset_router as dataset_router
from backend.app.services.ml_engine import GLOBAL_ML_ENGINE

router = APIRouter(prefix="/api/ml", tags=["Machine Learning"])

@router.get("/train")
@router.post("/train")
async def train_model():
    dataset_router.ensure_default_dataset()
    active_id = dataset_router.ACTIVE_DATASET_ID
    ds = dataset_router.STORED_DATASETS.get(active_id)
    pdf = ds["processed_df"] if ds else None
    
    if pdf is None or pdf.empty:
        raise HTTPException(status_code=400, detail="Processed dataset is empty.")
        
    try:
        results = GLOBAL_ML_ENGINE.train_model(pdf, dataset_id=active_id)
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict")
async def predict_review(request: Request):
    review_text = None
    
    # 1. Try parsing JSON payload
    try:
        body = await request.json()
        if isinstance(body, dict):
            review_text = body.get("text") or body.get("review") or body.get("comment")
    except Exception:
        pass
        
    # 2. Try parsing Form data payload
    if not review_text:
        try:
            form = await request.form()
            review_text = form.get("text") or form.get("review") or form.get("comment")
        except Exception:
            pass

    # 3. Try query parameters
    if not review_text:
        review_text = request.query_params.get("text") or request.query_params.get("review")

    if not review_text or not str(review_text).strip():
        raise HTTPException(status_code=400, detail="Please enter a review to classify.")
        
    review_text = str(review_text).strip()
    
    active_id = dataset_router.ACTIVE_DATASET_ID
    if active_id and GLOBAL_ML_ENGINE.dataset_id != active_id:
        GLOBAL_ML_ENGINE.invalidate_model()
        
    res = GLOBAL_ML_ENGINE.predict_sentiment(review_text)
    if res.get("status") == "error":
        raise HTTPException(status_code=400, detail=res.get("detail"))
        
    return res
