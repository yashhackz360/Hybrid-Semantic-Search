import nltk

# List of all required NLTK packages for this project
REQUIRED_PACKAGES = [
    'wordnet',
    'omw-1.4',
    'punkt',
    'punkt_tab',
    'averaged_perceptron_tagger'
]

print("Downloading required NLTK packages...")

for package in REQUIRED_PACKAGES:
    try:
        nltk.data.find(f"tokenizers/{package}")
    except LookupError:
        try:
            nltk.data.find(f"corpora/{package}")
        except LookupError:
            try:
                nltk.data.find(f"taggers/{package}")
            except LookupError:
                print(f"-> Downloading '{package}'...")
                nltk.download(package)

print("✅ All NLTK packages are ready.")