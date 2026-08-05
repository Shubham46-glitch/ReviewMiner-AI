import pandas as pd
import re
import string

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    
    # Download required NLTK resources
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    
    STOPWORDS = set(stopwords.words('english'))
    USE_NLTK = True
except ImportError:
    print("NLTK not found. Falling back to basic regex cleaning.")
    USE_NLTK = False
    STOPWORDS = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "should", "now"])

NEGATIONS = set(["no", "nor", "not", "neither", "never", "nobody", "none", "nothing", "nowhere", "without", "cannot", "cant", "don", "dont", "shouldn", "shouldnt", "wasn", "wasnt", "weren", "werent", "isn", "isnt", "aren", "arent", "hasn", "hasnt", "haven", "havent", "hadn", "hadnt", "wouldn", "wouldnt"])
STOPWORDS = STOPWORDS - NEGATIONS

def clean_text(text):
    if not isinstance(text, str):
        return ""
        
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove punctuation & special characters
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    
    # 3. Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 4. Tokenize and remove stopwords
    if USE_NLTK:
        try:
            words = word_tokenize(text)
        except Exception:
            words = text.split()
    else:
        words = text.split()
        
    cleaned_words = [w for w in words if w not in STOPWORDS]
    
    return " ".join(cleaned_words)

def main():
    print("Loading dataset...")
    df = pd.read_csv("product_reviews.csv")
    
    print(f"Original dataset shape: {df.shape}")
    print("Cleaning text data... this might take a moment.")
    
    # Apply cleaning function to the Text column
    if 'Text' in df.columns:
        df['Cleaned_Text'] = df['Text'].apply(clean_text)
        
        print("\nPreview of Cleaned Text:")
        print(df[['Text', 'Cleaned_Text']].head())
        
        # Save to a new CSV file
        output_file = "product_reviews_cleaned.csv"
        df.to_csv(output_file, index=False)
        print(f"\nSuccessfully saved cleaned dataset to {output_file}")
    else:
        print("Error: Could not find 'Text' column in the dataset.")

if __name__ == "__main__":
    main()
