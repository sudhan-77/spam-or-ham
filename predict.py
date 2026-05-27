import os
import sys
import argparse
import joblib

# Add current directory to path if run from elsewhere
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocess import TextPreprocessor

def load_classifier():
    """
    Loads the trained model and vectorizer.
    """
    model_path = os.path.join("models", "spam_classifier_model.pkl")
    vectorizer_path = os.path.join("models", "tfidf_vectorizer.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("Error: Trained model files not found in 'models/' directory.")
        print("Please run 'python src/train.py' first to train and save the model.")
        sys.exit(1)
        
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def predict_message(message, model, vectorizer, preprocessor):
    """
    Preprocesses a message, vectorizes it, and predicts whether it is spam or ham.
    """
    cleaned = preprocessor.preprocess(message)
    if not cleaned:
        # Fallback if text is empty after cleaning
        return "ham", 0.0
        
    features = vectorizer.transform([cleaned])
    prediction = model.predict(features)[0]
    
    # Estimate probability/confidence if supported
    confidence = 1.0
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features)[0]
        confidence = probabilities[prediction]
        
    label = "spam" if prediction == 1 else "ham"
    return label, confidence

def main():
    parser = argparse.ArgumentParser(description="SMS Spam/Ham Classifier Inference Tool")
    parser.add_argument("--message", type=str, help="Specific message to classify")
    args = parser.parse_args()
    
    # Load model and components
    model, vectorizer = load_classifier()
    preprocessor = TextPreprocessor()
    
    if args.message:
        # Single message mode
        label, conf = predict_message(args.message, model, vectorizer, preprocessor)
        print(f"\nMessage: \"{args.message}\"")
        print(f"Classification: {label.upper()}")
        print(f"Confidence: {conf*100:.2f}%")
    else:
        # Interactive mode
        print("\n" + "="*50)
        print("    SMS SPAM / HAM INTERACTIVE CLASSIFIER CLI    ")
        print("="*50)
        print("Type your message below to classify it.")
        print("Type 'exit' or 'quit' to close the program.\n")
        
        while True:
            try:
                message = input("Enter message > ")
                if message.strip().lower() in ['exit', 'quit']:
                    print("Exiting. Goodbye!")
                    break
                if not message.strip():
                    continue
                    
                label, conf = predict_message(message, model, vectorizer, preprocessor)
                
                # Visual enhancement
                color_start = "\033[91m" if label == "spam" else "\033[92m"
                color_reset = "\033[0m"
                
                print(f"Prediction: {color_start}{label.upper()}{color_reset} (Confidence: {conf*100:.2f}%)")
                print("-" * 50)
            except KeyboardInterrupt:
                print("\nExiting. Goodbye!")
                break

if __name__ == "__main__":
    main()
