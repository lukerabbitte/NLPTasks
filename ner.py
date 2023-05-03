import spacy

nlp = spacy.load("en_core_web_sm")

# Example database entry from LPM
text = "Acerra (Nap.) N 3260\n\tCathedral, with +Archives\n\tRuins of Roman Bath"

# Preprocess the text
text = text.lower().replace("\n", " ").replace("\t", " ")

# Tokenize the text
doc = nlp(text)

# Extract named entities
entities = [(ent.text, ent.label_) for ent in doc.ents]

# Post-process the results
site_name = ""
star_rating = ""

for i, (entity, label) in enumerate(entities):
    # Assume site name is the longest sequence of non-location words
    if label != "LOC" and len(entity) > len(site_name):
        site_name = entity

    # Assume star rating is the first number after the site name
    if entity.isdigit() and i > 0 and entities[i - 1][0] == site_name:
        star_rating = entity
        break

# Print the results
print("Site name:", site_name)
print("Star rating:", star_rating)