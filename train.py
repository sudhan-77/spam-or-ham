import os
import zipfile
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Import the text preprocessor we created
from preprocess import TextPreprocessor

# Ensure directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

def download_dataset():
    """
    Downloads the SMS Spam Collection dataset using multiple fallback URLs
    to ensure extremely high reliability.
    """
    output_path = os.path.join("data", "SMSSpamCollection")
    if os.path.exists(output_path):
        print(f"Dataset already exists at {output_path}. Skipping download.")
        return output_path

    # List of URLs to try:
    # 1. Standard raw TSV from a highly reliable GitHub repo
    # 2. UCI ML static zip new format
    # 3. UCI ML old database zip format
    urls = [
        {
            "url": "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv",
            "is_zip": False,
            "filename": "SMSSpamCollection"
        },
        {
            "url": "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip",
            "is_zip": True,
            "filename": "sms+spam+collection.zip"
        },
        {
            "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip",
            "is_zip": True,
            "filename": "smsspamcollection.zip"
        }
    ]

    for source in urls:
        url = source["url"]
        is_zip = source["is_zip"]
        filename = source["filename"]
        temp_path = os.path.join("data", filename)
        
        print(f"Attempting to download dataset from: {url}")
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                with open(temp_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded successfully to {temp_path}")
                
                if is_zip:
                    print("Extracting ZIP file...")
                    with zipfile.ZipFile(temp_path, "r") as zip_ref:
                        zip_ref.extractall("data")
                    
                    # Clean up zip
                    os.remove(temp_path)
                    
                    # The zip contains SMSSpamCollection or SMSspameCollection
                    # Standardize filename if needed
                    extracted_files = os.listdir("data")
                    for ef in extracted_files:
                        if ef.lower() == "smsspamcollection":
                            os.rename(os.path.join("data", ef), output_path)
                            break
                else:
                    # It's a raw text file (tsv)
                    if filename != "SMSSpamCollection":
                        os.rename(temp_path, output_path)
                
                if os.path.exists(output_path):
                    print(f"Dataset successfully prepared at {output_path}")
                    return output_path
            else:
                print(f"Failed with status code {response.status_code}")
        except Exception as e:
            print(f"Error downloading from {url}: {e}")
            
    raise RuntimeError("Could not download the dataset from any of the sources. Please check internet connection.")

def load_and_preprocess_data(file_path):
    """
    Loads the raw text dataset, parses label and text, and applies text preprocessing.
    """
    print("Loading dataset...")
    # The file is tab-separated with no header. Format is: label \t message
    df = pd.read_csv(file_path, sep='\t', header=None, names=['label', 'message'])
    
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    print("Class distribution:")
    print(df['label'].value_counts())
    
    # Initialize our preprocessor
    print("Preprocessing text messages (lowercasing, cleaning, stemming)...")
    preprocessor = TextPreprocessor()
    df['clean_message'] = df['message'].apply(preprocessor.preprocess)
    
    # Filter out rows where message became empty after cleaning
    df = df[df['clean_message'].str.strip() != '']
    print(f"Dataset size after cleaning empty rows: {df.shape[0]} rows.")
    
    # Map labels: ham -> 0, spam -> 1
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
    
    return df

def train_and_evaluate(df):
    """
    Splits data, trains Naive Bayes and Logistic Regression, and saves the best model.
    """
    X = df['clean_message']
    y = df['label_num']
    
    # Split into train and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
    
    # Feature extraction using TF-IDF Vectorizer
    print("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Initialize classifiers
    models = {
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000)
    }
    
    best_f1 = 0
    best_model_name = ""
    best_model = None
    results = {}
    
    for name, model in models.items():
        print(f"\n--- Training and Evaluating: {name} ---")
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)
        
        # Calculate metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "y_pred": y_pred
        }
        
        print(f"Accuracy : {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall   : {rec:.4f}")
        print(f"F1-Score : {f1:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))
        
        # We prioritize F1-score for evaluation (specifically the spam class)
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model = model

    print(f"\n==================================================")
    print(f"BEST MODEL CHOSEN: {best_model_name} (F1-Score: {best_f1:.4f})")
    print(f"==================================================")
    
    # Save the best model and vectorizer
    model_path = os.path.join("models", "spam_classifier_model.pkl")
    vectorizer_path = os.path.join("models", "tfidf_vectorizer.pkl")
    
    joblib.dump(best_model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Saved trained model to {model_path}")
    print(f"Saved TF-IDF vectorizer to {vectorizer_path}")
    
    # Plot and save confusion matrix for the best model
    best_preds = results[best_model_name]["y_pred"]
    cm = confusion_matrix(y_test, best_preds)
    
    plt.figure(figsize=(6, 5))
    sns.set_theme(style="whitegrid")
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'],
                annot_kws={"size": 14, "weight": "bold"})
    plt.title(f'Confusion Matrix\n({best_model_name})', fontsize=14, pad=15, weight='bold')
    plt.xlabel('Predicted Label', fontsize=12, labelpad=10)
    plt.ylabel('True Label', fontsize=12, labelpad=10)
    plt.tight_layout()
    
    plot_path = os.path.join("models", "confusion_matrix.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Saved Confusion Matrix visualization to {plot_path}")
    
    # Write metadata results file to easily load in generate_docs
    with open(os.path.join("models", "metrics.txt"), "w") as f:
        f.write(f"Model Name: {best_model_name}\n")
        f.write(f"Accuracy: {results[best_model_name]['accuracy']:.4f}\n")
        f.write(f"Precision: {results[best_model_name]['precision']:.4f}\n")
        f.write(f"Recall: {results[best_model_name]['recall']:.4f}\n")
        f.write(f"F1-Score: {results[best_model_name]['f1_score']:.4f}\n")
        f.write(f"True Negative (Ham classified as Ham): {cm[0][0]}\n")
        f.write(f"False Positive (Ham classified as Spam): {cm[0][1]}\n")
        f.write(f"False Negative (Spam classified as Ham): {cm[1][0]}\n")
        f.write(f"True Positive (Spam classified as Spam): {cm[1][1]}\n")

if __name__ == "__main__":
    try:
        data_path = download_dataset()
        df = load_and_preprocess_data(data_path)
        train_and_evaluate(df)
        print("\nModel pipeline completed successfully!")
    except Exception as e:
        print(f"\nError in training pipeline: {e}")
