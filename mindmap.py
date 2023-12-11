from dotenv import load_dotenv
import os
#import pygraphviz as pgv

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

template='''pos = graphviz_layout(G, prog="dot")
    node_labels = nx.get_node_attributes(G, 'label')
    node_sizes = [len(label) * 200 for label in node_labels]
    edge_labels = {}
    for edge in G.edges():
        node1, node2 = edge
        edge_labels[edge] = G[node1][node2]['label']
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=8, edge_color="gray", arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')'''

load_dotenv()

# def mindmap_test():
    
#     # Creazione del grafico
#     A = pgv.AGraph(directed=True, strict=True, rankdir='LR')

#     # Nodi principali
#     A.add_node("Rivoluzione Francese")

#     # Cause
#     A.add_node("Cause")
#     A.add_edge("Rivoluzione Francese", "Cause")
#     A.add_node("Crisi finanziaria")
#     A.add_edge("Cause", "Crisi finanziaria")
#     A.add_node("Disuguaglianza sociale")
#     A.add_edge("Cause", "Disuguaglianza sociale")
#     A.add_node("Idee illuministe")
#     A.add_edge("Cause", "Idee illuministe")

#     # Eventi principali
#     A.add_node("Eventi principali")
#     A.add_edge("Rivoluzione Francese", "Eventi principali")
#     A.add_node("Presa della Bastiglia")
#     A.add_edge("Eventi principali", "Presa della Bastiglia")
#     A.add_node("Regno del Terrore")
#     A.add_edge("Eventi principali", "Regno del Terrore")
#     A.add_node("Esecuzione di Luigi XVI")
#     A.add_edge("Eventi principali", "Esecuzione di Luigi XVI")

#     # Figure chiave
#     A.add_node("Figure chiave")
#     A.add_edge("Rivoluzione Francese", "Figure chiave")
#     A.add_node("Robespierre")
#     A.add_edge("Figure chiave", "Robespierre")
#     A.add_node("Luigi XVI")
#     A.add_edge("Figure chiave", "Luigi XVI")
#     A.add_node("Marie Antoinette")
#     A.add_edge("Figure chiave", "Marie Antoinette")

#     # Conseguenze
#     A.add_node("Conseguenze")
#     A.add_edge("Rivoluzione Francese", "Conseguenze")
#     A.add_node("Fine della monarchia")
#     A.add_edge("Conseguenze", "Fine della monarchia")
#     A.add_node("Ascesa di Napoleone Bonaparte")
#     A.add_edge("Conseguenze", "Ascesa di Napoleone Bonaparte")

#     # Aggiunta delle etichette agli archi
#     A.get_edge("Cause", "Crisi finanziaria").attr['label'] = 'portato da'
#     A.get_edge("Eventi principali", "Presa della Bastiglia").attr['label'] = 'incluso'
#     A.get_edge("Figure chiave", "Robespierre").attr['label'] = 'come'
#     A.get_edge("Conseguenze", "Fine della monarchia").attr['label'] = 'portato a'

#     # Layout e renderizzazione con le nuove etichette
#     A.layout(prog='dot')
#     A.draw("rivoluzione_francese_etichette.png")
   
# def execute_concept_map_code(code):
#     # Esegui il codice
#     exec(code)

# def json_code_test():
#     # Esempio di codice restituito in formato JSON
#     json_code = '''
#     graph = pgv.AGraph(directed=True)

#     # Nodo principale
#     graph.add_node("Cellula")

#     # Sottonodi con etichette agli archi
#     graph.add_node("Membrana Cellulare", shape="box")
#     graph.add_node("Nucleo", shape="box")
#     graph.add_node("Organelle", shape="box")

#     graph.add_edge("Cellula", "Membrana Cellulare", label="Struttura Esterna")
#     graph.add_edge("Cellula", "Nucleo", label="Centro di Controllo")
#     graph.add_edge("Cellula", "Organelle", label="Componenti Funzionali")

#     # Visualizzazione
#     graph.layout(prog="dot")
#     graph.draw("cellula_concept_map.png", format="png", prog="dot")
#     '''

#     execute_concept_map_code(json_code)

def execute_networkx():

    G = nx.Graph()
    G.add_node("atom", label="atom")
    G.add_node("nucleus", label="nucleus")
    G.add_node("protons", label="protons")
    G.add_node("neutrons", label="neutrons")
    G.add_node("electrons", label="electrons")
    G.add_edge("atom", "nucleus", label="contains")
    G.add_edge("nucleus", "protons", label="contains")
    G.add_edge("nucleus", "neutrons", label="contains")
    G.add_edge("atom", "electrons", label="contains")
    pos = graphviz_layout(G, prog="dot")
    node_labels = nx.get_node_attributes(G, 'label')
    node_sizes = [len(label) * 200 for label in node_labels]
    edge_labels = dict()
    for edge in G.edges():
        node1, node2 = edge
        edge_labels[edge] = G[node1][node2]['label']
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=8, edge_color="gray", arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')

    plt.savefig("atom.png")
    plt.show()

execute_networkx()