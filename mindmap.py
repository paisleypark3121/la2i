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
    G.add_node("jokerbirot", label="jokerbirot")
    G.add_node("musician", label="musician")
    G.add_node("impact", label="impact")
    G.add_node("return", label="return")
    G.add_edge("jokerbirot", "musician", label="is a")
    G.add_edge("jokerbirot", "impact", label="has on")
    G.add_edge("jokerbirot", "return", label="has a")
    pos = graphviz_layout(G, prog="dot")
    node_labels = nx.get_node_attributes(G, 'label')
    node_sizes = [len(label) * 200 for label in node_labels]
    edge_labels = dict()
    for edge in G.edges():
        node1, node2 = edge
        edge_labels[edge] = G[node1][node2]['label']
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=8, edge_color="gray", nodelist=list(G.nodes()))
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')
    #plt.savefig("jokerbirot.png")
    #plt.savefig("Stars.png")
    plt.show()

def execute_networkx2():

    net1 = """
font_size=14
mm = nx.Graph()
mm.clear()
mm.add_node("jokerbirot", label="jokerbirot")
mm.add_node("2077", label="2077")
mm.add_node("advanced technology", label="advanced technology")
mm.add_node("sci-fi movie", label="sci-fi movie")
mm.add_edge("jokerbirot", "2077", label="time setting")
mm.add_edge("2077", "advanced technology", label="characteristic")
mm.add_edge("jokerbirot", "sci-fi movie", label="comparison")
pos = graphviz_layout(mm, prog="dot")
node_labels = nx.get_node_attributes(mm, 'label')
node_sizes = [len(label) * 600 for label in node_labels.values()]
edge_lbls = dict()
for edge in mm.edges():
    node1, node2 = edge
    edge_lbls[edge] = mm[node1][node2]['label']
fig91, ax91 = plt.subplots(figsize=(20,15))
nx.draw(mm, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=font_size, edge_color="gray", nodelist=list(mm.nodes()), ax=ax91)
nx.draw_networkx_edge_labels(mm, pos, edge_labels=edge_lbls, font_size=font_size, font_color='red', ax=ax91)
fig91.savefig("jokerbirot.png")
fig91.show()
"""

#     net2 = """
# G2 = nx.Graph()
# G2.clear()
# G2.add_node("jokerbirot", label="jokerbirot")
# G2.add_node("musician", label="musician")
# G2.add_node("impact", label="impact")
# G2.add_edge("jokerbirot", "musician", label="is a")
# G2.add_edge("jokerbirot", "impact", label="has on")
# pos2 = graphviz_layout(G2, prog="dot")
# node_labels2 = nx.get_node_attributes(G2, 'label')
# node_sizes2 = [len(label) * 200 for label in node_labels2]
# edge_labels2 = dict()
# for edge in G2.edges():
#     node1, node2 = edge
#     edge_labels2[edge] = G2[node1][node2]['label']
# fig2, ax2 = plt.subplots()
# nx.draw(G2, pos2, with_labels=True, font_weight='bold', node_size=node_sizes2, node_color="skyblue", font_size=8, edge_color="gray", nodelist=list(G2.nodes()), ax=ax2)
# nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2, font_size=8, font_color='red', ax=ax2)
# fig2.savefig("jokerbirot_2.png")
#"""

    exec(net1)
    #exec(net2)

execute_networkx2()