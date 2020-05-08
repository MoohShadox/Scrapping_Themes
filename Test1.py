import json
import pandas as pd
import rdflib
g = rdflib.Graph()


contextes = []

def loadContextes():
    g.parse("sortie.rdf")
    request = """
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> 
    prefix owl_ns: <https://www.exemple.com#>
    prefix rdf_ns: <https://Data/>
    SELECT DISTINCT ?contenu ?r 
       WHERE {
       ?s rdf:type owl_ns:Question .
       ?s rdfs:label ?contenu . 
       ?s owl_ns:hasAnswer ?rep . 
       ?rep rdfs:label ?r
        }
    """
    g.query(request)

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(contextes)
print(X_train_counts.shape)

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print(X_train_tfidf.shape)


#X_train_counts = []
#

#


df = pd.DataFrame()


