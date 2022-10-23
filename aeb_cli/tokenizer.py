import spacy
#from spacy.tokenizer import Tokenizer
#from spacy.lang.en import English
#nlp = English()
# Create a blank Tokenizer with just the English vocab
#tokenizer = Tokenizer(nlp.vocab)

# Construction 2
from spacy.lang.en import English
nlp = English()
# Create a Tokenizer with the default settings for English
# including punctuation rules and exceptions
tokenizer = nlp.tokenizer

def tokenize(text):
    #for k, v in ob_dict['extracts'].items():
    #    tokens = tokenizer(v.articleBody)
    tokens = tokenizer(text)
    return [t.text for t in tokens]

def tokenize_pipe(ob_dict):
    breakpoint()
    texts = [v['articleBody'] for k, v in ob_dict['extracts'].items()]
    for doc in tokenizer.pipe(texts, batch_size=100):
        tokens = [token.text for token in doc]
        # pass