import threading
import time
from threading import Thread

import rdflib
import json

from Scrapping import search_google, get_Portails


owl_ns = "https://www.exemple.com#"
rdf_ns = "https://Data/"

g = rdflib.Graph()
verrou = threading.Lock()

D = json.load(open("train.json",encoding="utf8"))


class Scrapping_Thread(Thread):

    def __init__(self,word,graph,verrou):
        super().__init__()
        self.__word = word.strip()
        self.__result = []
        self.__graph_sec = graph,verrou
        print("Thread for ",self.__word, "created ! ")

    def run(self):
        if(len(self.__word.strip()) == 0):
            return
        link = search_google(self.__word.strip())[0]
        self.__result = get_Portails(link)
        print("Thread Fini : ",self.__result)
        with self.__graph_sec[1]:
            for r in self.__result:
                add_categorie(self.__graph_sec[0],self.__word,r)




def add_title(title):
    title_r = rdflib.URIRef(rdf_ns+"Title#"+title)
    titre_t = rdflib.URIRef( owl_ns+"Titre")
    g.add( (title_r,rdflib.RDF.term('type') , titre_t) )


def add_categorie(graph,title,cat):
    categorie_t = rdflib.URIRef(owl_ns + "Categorie")
    categorie_r = rdflib.URIRef(rdf_ns + cat)

    title_r = rdflib.URIRef(rdf_ns+"Title#"+title)

    hasCategorie = rdflib.URIRef(owl_ns + "hasCategorie")

    graph.add((categorie_r,rdflib.RDF.term('type') , categorie_t))
    graph.add((title_r,hasCategorie , categorie_r))


def add_contexte(title,contexte):
    title_r = rdflib.URIRef(rdf_ns + "Title#" + title)
    contexte_r = rdflib.URIRef(rdf_ns + "Contexte#" + title)
    contexte_t = rdflib.URIRef(owl_ns + "Contexte")
    hasContexte = rdflib.URIRef(owl_ns + "hasContexte")
    contexte_label = rdflib.Literal(contexte)
    g.add((contexte_r, rdflib.RDF.term('type'), contexte_t))
    g.add((title_r, hasContexte, contexte_r))
    g.add((contexte_r,rdflib.RDFS.term("label"),contexte_label))

def addQAS(title,question,answer,qid):
    title_r = rdflib.URIRef(rdf_ns + "Title#" + title)

    question_t = rdflib.URIRef(owl_ns + "Question")
    reponse_t = rdflib.URIRef(owl_ns + "Reponse")

    question_r = rdflib.URIRef(rdf_ns + "Question#" + qid)
    answer_r = rdflib.URIRef(rdf_ns + "Reponse#" + qid)

    g.add((question_r, rdflib.RDF.term('type'), question_t))
    g.add((answer_r, rdflib.RDF.term('type'), reponse_t))

    g.add((question_r,rdflib.RDFS.term("label"),rdflib.Literal(question)))
    g.add((answer_r,rdflib.RDFS.term("label"),rdflib.Literal(answer)))

    g.add((title_r,rdflib.URIRef(owl_ns+"relatedToQuestion"),question_t))
    g.add((title_r,rdflib.URIRef(owl_ns+"relatedToAnswer"),answer_r))
    g.add((question_r,rdflib.URIRef(owl_ns+"hasAnswer"),answer_r))



def request_All():
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
    qres = g.query(request)

    for row in qres:
        if(len(row[1].split(" ")) < 3):
            print(row[0] , row[1] )
    print("Total de question possibles : ",len(qres))




def mine_dataset(link):
    D = json.load(open(link, encoding="utf8"))
    contextes = []
    titres = []
    for i in D["data"]:
        print("paragraphe : ",i["paragraphs"])
        for k in i["paragraphs"]:
            for qas in k["qas"]:
                print("ID = ",qas["id"])
                print("Question : ",qas["question"])
                for t in qas["answers"]:
                    addQAS(i["title"], qas["question"], t["text"], qas["id"])
                    print("Answers : ",t["text"])
        titres.append(i["title"])
        add_title(i["title"])
        title = i["title"]
        for j in i["paragraphs"]:
            contextes.append(j["context"])
            add_contexte(title,j["context"])





def add_categories():
    with open("themes_list.txt","r",encoding="utf8") as f:
       step = 15
       L = f.readlines()
       for j in range(0,len(L),step):
            Threads = []
            for i in L[j:j+step-1]:
                T = Scrapping_Thread(i,g,verrou)
                T.start()
                Threads.append(T)
            for T in Threads:
                T.join()



def construction():
    mine_dataset("train.json")
    add_categories()
    g.serialize("sortie.rdf",format='turtle')


def time_printing(func):
    t = time.time()
    func()
    print("Loading en  : ",time.time() - t," s ")

def graphParse():
    g.parse("sortie.rdf",format='turtle')

loading = lambda :time_printing(graphParse)

request = """
    prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> 
    prefix : <https://www.exemple.com#>
    prefix rdf_ns: <https://Data/>
    SELECT DISTINCT ?lab ?rep
       WHERE {
       ?question rdf:type :Question .
       ?question rdfs:label ?lab .
       ?question :hasAnswer ?reponse .
       ?reponse rdfs:label ?rep
        }
    """
#construction()

loading()
request_All()

#print(contextes)
#print(titres)