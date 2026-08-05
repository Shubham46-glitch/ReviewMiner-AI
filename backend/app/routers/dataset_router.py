import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.app.services.text_engine import auto_detect_columns, predict_vader_sentiment, clean_text_full

router = APIRouter(prefix="/api/dataset", tags=["Dataset"])

# Global session storage for active datasets in memory
STORED_DATASETS = {}
ACTIVE_DATASET_ID = None

def read_uploaded_file(file: UploadFile) -> pd.DataFrame:
    content = file.file.read()
    name = file.filename.lower()
    
    if name.endswith('.xlsx') or name.endswith('.xls'):
        return pd.read_excel(io.BytesIO(content))
        
    if name.endswith('.txt'):
        text_str = content.decode('utf-8', errors='ignore')
        lines = [line.strip() for line in text_str.split('\n') if line.strip()]
        return pd.DataFrame({"Text": lines})
        
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    for enc in encodings:
        try:
            sep = '\t' if name.endswith('.tsv') else ','
            df = pd.read_csv(io.BytesIO(content), encoding=enc, sep=sep)
            return df
        except Exception:
            continue
            
    return pd.read_csv(io.BytesIO(content), on_bad_lines='skip')

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    global ACTIVE_DATASET_ID
    try:
        df = read_uploaded_file(file)
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            
        auto_text, auto_label, auto_plat = auto_detect_columns(df)
        dataset_id = file.filename
        
        STORED_DATASETS[dataset_id] = {
            "name": file.filename,
            "raw_df": df,
            "processed_df": None,
            "text_col": auto_text,
            "label_col": auto_label,
            "plat_col": auto_plat,
            "has_labels": auto_label is not None
        }
        ACTIVE_DATASET_ID = dataset_id
        
        # Auto-process with defaults
        process_dataset(dataset_id, auto_text, auto_label, auto_plat)
        
        cols = df.columns.tolist()
        return {
            "status": "success",
            "dataset_id": dataset_id,
            "filename": file.filename,
            "row_count": len(df),
            "col_count": len(cols),
            "columns": cols,
            "detected": {
                "text_col": auto_text,
                "label_col": auto_label,
                "platform_col": auto_plat
            },
            "preview": df.head(5).fillna("").to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process dataset: {str(e)}")

def process_dataset(dataset_id: str, text_col: str, label_col: str = None, plat_col: str = None):
    if dataset_id not in STORED_DATASETS:
        return
    ds = STORED_DATASETS[dataset_id]
    raw_df = ds["raw_df"].copy()
    
    if text_col not in raw_df.columns:
        raise ValueError(f"Text column '{text_col}' not found.")
        
    df = pd.DataFrame()
    df["Text"] = raw_df[text_col].astype(str).fillna("")
    
    if label_col and label_col in raw_df.columns:
        def map_lbl(v):
            if pd.isna(v) or v is None: return "Neutral"
            vs = str(v).strip().lower()
            if vs in ['positive', 'pos', '5', '4', 'high', 'good']: return 'Positive'
            elif vs in ['negative', 'neg', '0', '-1', '2', 'low', 'bad']: return 'Negative'
            elif vs in ['neutral', 'neu', '3', 'medium']: return 'Neutral'
            try:
                num = float(v)
                return 'Positive' if num >= 4 else ('Negative' if num <= 2 else 'Neutral')
            except Exception:
                return str(v).capitalize()
        df["Label"] = raw_df[label_col].apply(map_lbl)
        ds["has_labels"] = True
    else:
        df["Label"] = df["Text"].apply(predict_vader_sentiment)
        ds["has_labels"] = False
        
    if plat_col and plat_col in raw_df.columns:
        df["Window"] = raw_df[plat_col].astype(str).fillna("General")
    else:
        df["Window"] = "Uploaded Data"
        
    df["Cleaned_Text"] = df["Text"].apply(clean_text_full)
    df["Cleaned_Text"] = df.apply(lambda r: r["Cleaned_Text"] if r["Cleaned_Text"].strip() != "" else r["Text"].lower(), axis=1)
    df = df[df["Text"].str.strip() != ""].reset_index(drop=True)
    
    ds["processed_df"] = df
    ds["text_col"] = text_col
    ds["label_col"] = label_col
    ds["plat_col"] = plat_col

@router.post("/map")
async def map_columns(dataset_id: str = Form(...), text_col: str = Form(...), label_col: str = Form(None), plat_col: str = Form(None)):
    if dataset_id not in STORED_DATASETS:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    try:
        final_label = None if label_col in [None, "", "null", "None"] else label_col
        final_plat = None if plat_col in [None, "", "null", "None"] else plat_col
        process_dataset(dataset_id, text_col, final_label, final_plat)
        return {"status": "success", "message": "Columns mapped and pipeline re-executed successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/active")
async def get_active_dataset_info():
    if not ACTIVE_DATASET_ID or ACTIVE_DATASET_ID not in STORED_DATASETS:
        return {"active": False, "message": "No active dataset loaded."}
    ds = STORED_DATASETS[ACTIVE_DATASET_ID]
    pdf = ds["processed_df"]
    return {
        "active": True,
        "dataset_id": ACTIVE_DATASET_ID,
        "name": ds["name"],
        "row_count": len(pdf) if pdf is not None else 0,
        "has_labels": ds["has_labels"],
        "columns": ds["raw_df"].columns.tolist(),
        "mapped": {
            "text_col": ds["text_col"],
            "label_col": ds["label_col"],
            "plat_col": ds["plat_col"]
        }
    }

@router.get("/compare")
async def compare_datasets():
    if len(STORED_DATASETS) < 2:
        return {"can_compare": False, "message": "Upload at least 2 datasets to perform comparison."}
    
    comparison = []
    for did, ds in STORED_DATASETS.items():
        pdf = ds["processed_df"]
        if pdf is not None and not pdf.empty:
            total = len(pdf)
            pos = len(pdf[pdf["Label"] == "Positive"])
            neg = len(pdf[pdf["Label"] == "Negative"])
            neu = len(pdf[pdf["Label"] == "Neutral"])
            avg_len = float(pdf["Text"].astype(str).str.len().mean())
            comparison.append({
                "dataset_name": ds["name"],
                "total_records": total,
                "positive_pct": round(pos / total * 100, 1) if total > 0 else 0,
                "negative_pct": round(neg / total * 100, 1) if total > 0 else 0,
                "neutral_pct": round(neu / total * 100, 1) if total > 0 else 0,
                "avg_text_length": round(avg_len, 1)
            })
    return {"can_compare": True, "datasets": comparison}
