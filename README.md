# NLP-Task
🧠 Natural Language Processing – Text Preprocessing Project

This project showcases a comprehensive text preprocessing pipeline using Natural Language Toolkit (NLTK). It includes tokenization, stopword removal, lemmatization, and part-of-speech tagging – foundational steps in building any NLP model.
📝 Project Objective

To apply key NLP preprocessing tasks on sample raw text data, demonstrating how raw language can be cleaned, structured, and prepared for downstream tasks such as sentiment analysis, classification, or language modeling.
📚 Libraries Used
    nltk.tokenize.punkt – For sentence and word tokenization
    nltk.corpus.stopwords – For removing common words
    nltk.corpus.wordnet – For lemmatization using WordNet
    nltk.data.load('tokenizers/punkt/english.pickle') – For sentence segmentation
    nltk.tag – Part-of-speech tagging with averaged_perceptron_tagger

🔍 Key Preprocessing Steps
1. Text Tokenization
   Sentence Tokenization using punkt
   Word Tokenization using word_tokenize

2. Stopword Removal
   Removed commonly used English stopwords like "the", "is", "in", etc. using stopwords.words('english')

3. Lemmatization
   Converted words to their base form using WordNetLemmatizer
   Mapped POS tags to WordNet format for accurate lemmatization

4. Part-of-Speech (POS) Tagging
   Tagged each word with its grammatical role using nltk.pos_tag
   Visualized tagged tokens
