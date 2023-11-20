from dotenv import load_dotenv
import os
import pygraphviz as pgv


load_dotenv()

def mindmap_test():
    
    # Creazione del grafico
    A = pgv.AGraph(directed=True, strict=True, rankdir='LR')

    # Nodi principali
    A.add_node("Rivoluzione Francese")

    # Cause
    A.add_node("Cause")
    A.add_edge("Rivoluzione Francese", "Cause")
    A.add_node("Crisi finanziaria")
    A.add_edge("Cause", "Crisi finanziaria")
    A.add_node("Disuguaglianza sociale")
    A.add_edge("Cause", "Disuguaglianza sociale")
    A.add_node("Idee illuministe")
    A.add_edge("Cause", "Idee illuministe")

    # Eventi principali
    A.add_node("Eventi principali")
    A.add_edge("Rivoluzione Francese", "Eventi principali")
    A.add_node("Presa della Bastiglia")
    A.add_edge("Eventi principali", "Presa della Bastiglia")
    A.add_node("Regno del Terrore")
    A.add_edge("Eventi principali", "Regno del Terrore")
    A.add_node("Esecuzione di Luigi XVI")
    A.add_edge("Eventi principali", "Esecuzione di Luigi XVI")

    # Figure chiave
    A.add_node("Figure chiave")
    A.add_edge("Rivoluzione Francese", "Figure chiave")
    A.add_node("Robespierre")
    A.add_edge("Figure chiave", "Robespierre")
    A.add_node("Luigi XVI")
    A.add_edge("Figure chiave", "Luigi XVI")
    A.add_node("Marie Antoinette")
    A.add_edge("Figure chiave", "Marie Antoinette")

    # Conseguenze
    A.add_node("Conseguenze")
    A.add_edge("Rivoluzione Francese", "Conseguenze")
    A.add_node("Fine della monarchia")
    A.add_edge("Conseguenze", "Fine della monarchia")
    A.add_node("Ascesa di Napoleone Bonaparte")
    A.add_edge("Conseguenze", "Ascesa di Napoleone Bonaparte")

    # Aggiunta delle etichette agli archi
    A.get_edge("Cause", "Crisi finanziaria").attr['label'] = 'portato da'
    A.get_edge("Eventi principali", "Presa della Bastiglia").attr['label'] = 'incluso'
    A.get_edge("Figure chiave", "Robespierre").attr['label'] = 'come'
    A.get_edge("Conseguenze", "Fine della monarchia").attr['label'] = 'portato a'

    # Layout e renderizzazione con le nuove etichette
    A.layout(prog='dot')
    A.draw("rivoluzione_francese_etichette.png")

    
def execute_concept_map_code(code):
    # Esegui il codice
    exec(code)

# Esempio di codice restituito in formato JSON
json_code = '''
graph = pgv.AGraph(directed=True)

# Nodo principale
graph.add_node("Cellula")

# Sottonodi con etichette agli archi
graph.add_node("Membrana Cellulare", shape="box")
graph.add_node("Nucleo", shape="box")
graph.add_node("Organelle", shape="box")

graph.add_edge("Cellula", "Membrana Cellulare", label="Struttura Esterna")
graph.add_edge("Cellula", "Nucleo", label="Centro di Controllo")
graph.add_edge("Cellula", "Organelle", label="Componenti Funzionali")

# Visualizzazione
graph.layout(prog="dot")
graph.draw("cellula_concept_map.png", format="png", prog="dot")
'''

# Chiamare la funzione per eseguire il codice
#execute_concept_map_code(json_code)

#mindmap_test()

from gtts import gTTS 
from io import BytesIO
import pygame

text = "Hello World!"

# get audio from server
tts = gTTS(text=text, lang='en')

# convert to file-like object
fp = BytesIO()
tts.write_to_fp(fp)
fp.seek(0)

# --- play it ---

import pygame

print('fp')

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(fp)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)