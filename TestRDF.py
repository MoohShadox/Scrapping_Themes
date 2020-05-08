import rdflib

#owl_ns = "http://www.semanticweb.org/ouagu/ontologies/2020/3/untitled-ontology-2#"
g = rdflib.Graph()


g.parse("sortie.rdf", format='turtle')

 """
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> 
    prefix : <http://www.semanticweb.org/ouagu/ontologies/2020/3/untitled-ontology-2#> .
    prefix rdf_ns: <https://Data/>
    
    SELECT DISTINCT ?cours ?salle 
       WHERE {
       ?touz rdf:type :Enseignant_RO .
       ?touz :enseigne ?module .
       ?module :ModuleADesCours ?cours .
       ?salle :acceuille ?cours .
        }
    """