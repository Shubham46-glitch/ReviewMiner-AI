import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers.dataset_router import router as dataset_router
from backend.app.routers.analytics_router import router as analytics_router
from backend.app.routers.ml_router import router as ml_router

app = FastAPI(
    title="ReviewMiner AI - REST API Engine",
    description="Enterprise NLP, Sentiment Analysis, and Machine Learning API Subsystem",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dataset_router)
app.include_router(analytics_router)
app.include_router(ml_router)

@app.get("/")
@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "ReviewMiner AI FastAPI Engine",
        "version": "2.0.0",
        "nlp_engine": "Active (NLTK, Scikit-Learn, VADER)"
    }

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
