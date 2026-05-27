import re
import string

# Hardcoded fallback list of common English stopwords in case nltk download is unavailable
FALLBACK_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

# Try to import nltk, but fall back gracefully if not available yet
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    
    # We will download resources on-demand in the train script, but define fallback here
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

class TextPreprocessor:
    def __init__(self):
        self.stemmer = None
        self.stopwords_set = FALLBACK_STOPWORDS
        
        if NLTK_AVAILABLE:
            try:
                # Try downloading nltk resources quietly
                nltk.download('stopwords', quiet=True)
                nltk.download('punkt', quiet=True)
                self.stopwords_set = set(stopwords.words('english'))
                self.stemmer = PorterStemmer()
            except Exception:
                # Fallback to hardcoded stopwords and no stemmer if NLTK downloads fail
                self.stopwords_set = FALLBACK_STOPWORDS
                self.stemmer = None

    def clean_text(self, text):
        """
        Cleans input text by:
        1. Converting to lowercase.
        2. Removing URLs, email addresses, and HTML tags.
        3. Removing punctuation and special characters.
        4. Removing numbers.
        """
        if not isinstance(text, str):
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove punctuation and special characters (replace with space to keep words separate)
        text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
        
        # Remove numbers/digits
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def preprocess(self, text):
        """
        Full preprocessing pipeline:
        1. Clean text.
        2. Tokenize by splitting whitespace.
        3. Remove stopwords.
        4. Apply Porter stemming (if NLTK stemmer is available).
        5. Re-join tokens into a single clean string.
        """
        cleaned = self.clean_text(text)
        tokens = cleaned.split()
        
        # Remove stopwords
        tokens = [word for word in tokens if word not in self.stopwords_set]
        
        # Apply stemming if available
        if self.stemmer:
            tokens = [self.stemmer.stem(word) for word in tokens]
            
        # Filter out very short tokens (length < 2)
        tokens = [word for word in tokens if len(word) >= 2]
        
        return " ".join(tokens)

if __name__ == "__main__":
    # Quick self-test
    preprocessor = TextPreprocessor()
    test_msg = "Congratulations! You've won 1,000,000 dollars! Click http://win.com now!"
    print(f"Original: {test_msg}")
    print(f"Cleaned : {preprocessor.clean_text(test_msg)}")
    print(f"Preprocessed: {preprocessor.preprocess(test_msg)}")
