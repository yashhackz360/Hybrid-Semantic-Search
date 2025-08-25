import nltk
from functools import lru_cache
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize

# --- NLTK Data Check ---
# This ensures all required packages are available.
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
# --- Configuration ---

# Words that WordNet often misinterprets in a tech context
DO_NOT_EXPAND = {'ram', 'core', 'thread', 'gb', 'windows', 'os'}

# Words that are noisy or irrelevant as synonyms
BLACKLIST = {
    "windowpane", "dingle", "pane", "computing_machine", "computing_device",
    "electronic_computer", "microcomputer", "window"
}

# Brands to skip during expansion
BRANDS = {"hp","dell","lenovo","asus","acer","apple","msi","huawei","xiaomi",
          "toshiba","samsung","google","microsoft","razer","lg"}

# --- Helper Functions ---

def _is_valid_synonym(word: str, term: str) -> bool:
    """Checks if a potential synonym is valid and not noisy."""
    if not word: return False
    lower_word = word.lower()
    if lower_word == term.lower(): return False
    if lower_word in BLACKLIST: return False
    
    parts = lower_word.split()
    if len(parts) > 2: return False # Avoid long, phrase-like synonyms
    if not all(p.isalpha() for p in parts): return False
    return True

def _map_pos_to_wordnet(pos_tag_str: str):
    """Maps Penn Treebank POS tags to WordNet POS tags."""
    if pos_tag_str.startswith("J"): return wn.ADJ
    if pos_tag_str.startswith("V"): return wn.VERB
    if pos_tag_str.startswith("N"): return wn.NOUN
    if pos_tag_str.startswith("R"): return wn.ADV
    return None

@lru_cache(maxsize=2048)
def _get_synonyms(term: str, wn_pos, max_synonyms: int = 2) -> list[str]:
    """
    Gets a deterministic, cached, and filtered list of synonyms for a term.
    """
    candidates = []
    synsets = wn.synsets(term, pos=wn_pos) if wn_pos else wn.synsets(term)
    
    for syn in sorted(synsets, key=lambda s: s.name()):
        for lemma in sorted(syn.lemmas(), key=lambda lem: lem.name()):
            candidates.append(lemma.name().replace("_", " "))

    seen = set()
    output_synonyms = []
    for word in candidates:
        lower_word = word.lower()
        if lower_word in seen: continue
        if _is_valid_synonym(word, term):
            seen.add(lower_word)
            output_synonyms.append(word)
            if len(output_synonyms) >= max_synonyms: break
    return output_synonyms

# --- Main Expansion Function ---

def expand_terms(
    text: str,
    pos_allow=("NN","NNS","JJ"), # Nouns and Adjectives
    max_synonyms=2,
):
    """
    Expands a query by appending relevant synonyms in parentheses
    next to the original words, preserving the query structure.
    """
    tokens = word_tokenize(text)
    tagged = pos_tag(tokens)
    output_tokens = []

    for (token, pos) in tagged:
        output_tokens.append(token) # Always add the original token to the output
        lower_token = token.lower()

        # --- Optimization Checks: Skip unnecessary words ---
        if not lower_token.isalpha(): continue # Skips '16GB', '₹85,000'
        if lower_token in STOPWORDS: continue # Skips 'with', 'a', 'for'
        if lower_token in DO_NOT_EXPAND: continue # Skips 'ram', 'core'
        if lower_token in BRANDS: continue # Skips 'hp', 'dell'
        if pos not in pos_allow: continue
        # --- End Checks ---
        
        wn_pos = _map_pos_to_wordnet(pos)
        synonyms = _get_synonyms(lower_token, wn_pos=wn_pos, max_synonyms=max_synonyms)

        # Append synonyms in a structured way
        if synonyms:
            output_tokens.append(f"({', '.join(synonyms)})")

    return " ".join(output_tokens)
