import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from backend.app.services.text_engine import clean_text_full, predict_vader_sentiment

class MLEngine:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.classes = []

    def train_model(self, df: pd.DataFrame, text_col: str = 'Cleaned_Text', label_col: str = 'Label'):
        if df.empty or text_col not in df.columns or label_col not in df.columns:
            raise ValueError("Invalid dataframe or missing columns for training.")
        
        valid_df = df[df[text_col].astype(str).str.strip() != ""].reset_index(drop=True)
        if len(valid_df) < 2 or valid_df[label_col].nunique() < 2:
            raise ValueError("Training requires at least 2 samples and at least 2 distinct sentiment classes.")

        X = valid_df[text_col].astype(str)
        y = valid_df[label_col].astype(str)
        
        try:
            self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
            X_vec = self.vectorizer.fit_transform(X)
        except Exception:
            self.vectorizer = TfidfVectorizer(max_features=5000)
            X_vec = self.vectorizer.fit_transform(X)
            
        class_counts = y.value_counts()
        can_stratify = (y.nunique() > 1) and (class_counts.min() >= 2) and (len(y) >= 5)
        
        if can_stratify:
            X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42, stratify=y)
        elif len(y) >= 4:
            X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
        else:
            X_train, X_test, y_train, y_test = X_vec, X_vec, y, y

        self.model = MultinomialNB()
        self.model.fit(X_train, y_train)
        self.classes = sorted(y.unique().tolist())

        y_pred = self.model.predict(X_test)
        
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average='weighted', zero_division=0))
        rec = float(recall_score(y_test, y_pred, average='weighted', zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average='weighted', zero_division=0))

        cm = confusion_matrix(y_test, y_pred, labels=self.classes).tolist()
        report = classification_report(y_test, y_pred, target_names=self.classes, output_dict=True, zero_division=0)

        return {
            "metrics": {
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "vocab_size": len(self.vectorizer.vocabulary_),
                "train_samples": X_train.shape[0],
                "test_samples": X_test.shape[0]
            },
            "confusion_matrix": {
                "labels": self.classes,
                "matrix": cm
            },
            "classification_report": report
        }

    def predict_sentiment(self, text: str):
        cleaned = clean_text_full(text)
        if self.model and self.vectorizer:
            try:
                X_in = self.vectorizer.transform([cleaned])
                pred = self.model.predict(X_in)[0]
                probs = self.model.predict_proba(X_in)[0]
                prob_dict = {cls: float(np.round(p * 100, 2)) for cls, p in zip(self.model.classes_, probs)}
                confidence = float(np.round(np.max(probs) * 100, 2))
                return {
                    "sentiment": pred,
                    "confidence": confidence,
                    "probabilities": prob_dict,
                    "model_used": "Trained Naive Bayes ML Model"
                }
            except Exception:
                pass
                
        # Fallback to VADER / Lexicon
        rule_pred = predict_vader_sentiment(cleaned or text)
        if rule_pred == "Positive":
            probs = {"Positive": 80.0, "Neutral": 15.0, "Negative": 5.0}
        elif rule_pred == "Negative":
            probs = {"Positive": 5.0, "Neutral": 15.0, "Negative": 80.0}
        else:
            probs = {"Positive": 15.0, "Neutral": 70.0, "Negative": 15.0}
            
        return {
            "sentiment": rule_pred,
            "confidence": 80.0,
            "probabilities": probs,
            "model_used": "Rule-Based VADER Lexicon Model"
        }

GLOBAL_ML_ENGINE = MLEngine()
