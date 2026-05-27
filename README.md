# 📱 SMS Spam Classifier: Machine Learning Pipeline

A high-performance, lightweight Machine Learning classification pipeline developed in Python to distinguish between **Spam** (unsolicited commercial ads, phishing, scam) and **Ham** (legitimate personal communication) messages. 

This project implements advanced text preprocessing (regex cleaning, lowercase folding, stopword removal, stemming), TF-IDF vectorization, and compares **Multinomial Naive Bayes** against a **Logistic Regression** baseline. It also contains a programmatic Word Document compiler to generate comprehensive academic-grade reports.

---

## 🚀 Performance Summary

Our trained **Multinomial Naive Bayes** classifier achieves outstanding results on unseen test data:

| Metric | Score | Detail |
|:---|:---:|:---|
| **Accuracy** | **~98.4%** | Overall correct predictions |
| **Precision** | **~98.5%** | Minimizing false positives (Ham classified as Spam) |
| **Recall** | **~89.2%** | Catching actual spam messages |
| **F1-Score** | **~93.6%** | Balanced performance metric |

> [!NOTE]
> High **Precision** is extremely critical in Spam filtering to ensure that important, legitimate user messages (Ham) are never accidentally marked as Spam and discarded. Our model achieves a **~98.5% precision rate**, resulting in almost zero false positives!

---

## 📁 Repository Structure

```text
spam_classifier/
│
├── data/
│   └── sms_spam_collection_raw.txt (UCI SMS Spam raw dataset - downloaded automatically)
│
├── models/
│   ├── confusion_matrix.png         (Generated confusion matrix heatmap)
│   ├── metrics.txt                  (Trained model performance values)
│   ├── spam_classifier_model.pkl   (Serialized Multinomial Naive Bayes model)
│   └── tfidf_vectorizer.pkl         (Serialized TF-IDF Vectorizer)
│
├── src/
│   ├── __init__.py
│   ├── preprocess.py                (Text cleaning, tokenization, and Porter stemming)
│   ├── train.py                     (Downloads dataset, preprocesses, trains, and evaluates models)
│   ├── predict.py                   (Command-line and interactive message classifier)
│   └── generate_docs.py             (Programmatic Word Document compiler)
│
├── README.md                        (Project overview and execution guide)
├── requirements.txt                 (Python package dependencies)
├── .gitignore                       (Excludes cache, raw data, and serialized weights)
└── Spam_Classifier_Documentation.docx (Programmatically generated professional report)
```

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.8+** installed. Follow these quick steps to set up and run the project:

### 1. Clone & Set Up Directory
Open your terminal inside the project directory:
```bash
# Navigate to the project folder (if not already there)
cd spam_classifier
```

### 2. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 3. Run the Training Pipeline
Execute the training script. This script will automatically download the dataset from secure mirrors, preprocess the text, train the models, select the best one, output the classification report, and save the confusion matrix heatmap:
```bash
python src/train.py
```

### 4. Classify Messages (Inference)
You can classify any custom message directly from the command line:
```bash
python src/predict.py --message "Congratulations! You've won a $1,000 Walmart gift card! Call 1-800-FREE-NOW to claim."
```

Or, run it without arguments to launch a **friendly, interactive CLI loop**:
```bash
python src/predict.py
```

### 5. Generate Professional Word Report
Generate the detailed Word document (`Spam_Classifier_Documentation.docx`) containing the dataset analysis, pipeline design, mathematical methodologies, performance matrices, and confusion matrix charts:
```bash
python src/generate_docs.py
```

---

## 💻 Technical Methodology

### 1. Text Preprocessing
The raw message text is cleaned through our pipeline (`src/preprocess.py`):
1. **Case Folding**: All text is lowercased.
2. **Entity Stripping**: URLs, emails, and HTML tags are removed.
3. **Punctuation & Digit Removal**: Non-alphabetical characters are stripped out.
4. **Stopword Removal**: High-frequency filler words (e.g. *the, in, of, at*) are filtered.
5. **Stemming**: Words are truncated to their base root using the **Porter Stemmer** (e.g. *winning, wins, won* $\rightarrow$ *win*).

### 2. Feature Engineering
We utilize **TF-IDF (Term Frequency-Inverse Document Frequency) Vectorization** to turn text tokens into a numerical representation:
* **Max Features**: 5,000
* **N-gram Range**: (1, 2) (extracts both individual words and word pairs to capture context)

### 3. Machine Learning Algorithms
* **Multinomial Naive Bayes (MNB)**: A probabilistic model utilizing Bayes' theorem with the assumption of feature independence. MNB is highly efficient, scale-invariant, and extremely accurate for text frequency data.
* **Logistic Regression (LR)**: A linear classifier serving as our baseline.

---

## 📤 Push to GitHub (Submission Guide)

To submit this project before your 3:00 PM deadline, follow these steps to push your repository to GitHub:

1. Create a new repository on [GitHub](https://github.com/new) named `spam-classifier` (keep it empty, do not initialize with README or gitignore).
2. Open your terminal in the `spam_classifier` directory.
3. Initialize the git repo, stage files, and commit:
   ```bash
   git init
   git add .
   git commit -m "feat: complete machine learning spam classifier pipeline and docs"
   ```
4. Link it to your GitHub and push:
   ```bash
   git branch -M main
   git remote add origin <YOUR_GITHUB_REPO_URL>
   git push -u origin main
   ```
   *(Replace `<YOUR_GITHUB_REPO_URL>` with your actual repository URL, e.g. `https://github.com/username/spam-classifier.git`)*
