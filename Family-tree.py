import spacy
import networkx as nx

# Load spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

# Sample input
text = "John is the father of Mary and Tom. Mary is married to David. David is the brother of Susan."

# Define relationships to look for
relations = {
    "father": "parent",
    "married": "spouse",
    "brother": "sibling"
}

# Initialize graph for family tree
family_tree = nx.DiGraph()

def parse_family(text):
    doc = nlp(text)
    for sent in doc.sents:
        entities = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
        if entities:
            for rel in relations.keys():
                if rel in sent.text:
                    relation_type = relations[rel]
                    if rel == "father":
                        # Parent-child relation
                        parent = entities[0]
                        for child in entities[1:]:
                            family_tree.add_edge(parent, child, relation=relation_type)
                    elif rel == "married":
                        # Spouse relation
                        family_tree.add_edge(entities[0], entities[1], relation=relation_type)
                    elif rel == "brother":
                        # Sibling relation
                        family_tree.add_edge(entities[0], entities[1], relation=relation_type)
                        
# Parse input text
parse_family(text)

# Print family tree
for edge in family_tree.edges(data=True):
    print(f"{edge[0]} is {edge[2]['relation']} of {edge[1]}")
