import nltk
from nltk.corpus import stopwords

with open('Resultat.txt', 'r') as file:
    text = file.read().rstrip()

# Step 1: Tokenize the text
tokens = nltk.word_tokenize(text)

# Step 2: Remove stop words
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if not word.lower() in stop_words]

# Step 3: Perform POS tagging
pos_tags = nltk.pos_tag(filtered_tokens)

# Step 4: Extract keywords
keywords = []
for word, tag in pos_tags:
    if tag.startswith('N'): # Nouns and Adjectives only
        keywords.append(word)

print(keywords);