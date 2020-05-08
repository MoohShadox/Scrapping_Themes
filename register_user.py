import rdflib
import time

def time_printing(func):
    t = time.time()
    func()
    print("Loading en  : ",time.time() - t," s ")


def graphParse(g):
    g.parse("sortie.rdf",format='turtle')

loading = lambda :time_printing(graphParse)

def register_user(name,quest):
    owl_ns = "https://www.exemple.com#"
    rdf_ns = "https://Data/"
    g = rdflib.Graph()
    g.parse("sortie.rdf",format='turtle')
    user_t = rdflib.URIRef(owl_ns+"User")
    user_c = rdflib.URIRef(rdf_ns+name)
    g.add((user_c,rdflib.RDF.term("type"),user_t))
    for att,val in quest.items():
        g.add((user_c,rdflib.URIRef(owl_ns+att),rdflib.Literal(val)))
    g.serialize("sortie.rdf",format='turtle')
    pass


import sys
D = {}

print("Ajout du user : ",sys.argv[1])
for i in range(2,len(sys.argv)):
    param = sys.argv[i]
    D[param.split("=")[0]] = param.split("=")[1]

register_user(sys.argv[1],D)