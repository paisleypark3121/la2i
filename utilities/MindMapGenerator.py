import json
from openai import OpenAI
import time

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

template = """You are a helpful assistant that generates a coded Mind Map given a specific [topic] and a [context].
Each map has to contain a maximum of 3 concepts and all connections must be labelled.
The output has to be the NetworkX python code needed to produce the mind map. This output has to contain only the code needed without any import.
As an example, the output has to start with: 
mm = nx.Graph(); 
As an example, if the user asks for: 
[topic] atom
[context] An atom is the fundamental building block of matter, consisting of two main components: electrons and nucleus. Electrons are negatively charged subatomic particles that orbit the nucleus in specific energy levels or electron shells; the nucleus is the central, densely packed core of an atom, where most of its mass is concentrated and contains two types of particles: protons (positively charged subatomic particles) and neutrons (electrically neutral subatomic particles).

coded mind map:
mm = nx.Graph()
mm.clear()
mm.add_node("atom", label="atom")
mm.add_node("nucleus", label="nucleus")
mm.add_node("protons", label="protons")
mm.add_node("neutrons", label="neutrons")
mm.add_node("electrons", label="electrons")
mm.add_edge("atom", "nucleus", label="composition")
mm.add_edge("nucleus", "protons", label="compositions")
mm.add_edge("nucleus", "neutrons", label="composition")
mm.add_edge("atom", "electrons", label="composition")
pos = graphviz_layout(mm, prog="dot")
node_labels = nx.get_node_attributes(mm, 'label')
node_sizes = [len(label) * 500 for label in node_labels]
edge_lbls = dict()
for edge in mm.edges():
    node1, node2 = edge
    edge_lbls[edge] = G[node1][node2]['label']
figure, axx = plt.subplots(figsize=(20,15))
font_size=14
nx.draw(mm, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=font_size, edge_color="gray", nodelist=list(mm.nodes()), ax=axx)
nx.draw_networkx_edge_labels(mm, pos, edge_labels=edge_lbls, font_size=font_size, font_color='red', ax=axx)'''
[topic]{topic}
[context]{context}

coded mind map:"""


def generateMindMap_mono_topic(name,text,temperature=0,model_name='gpt-4-0613'):

    #print(model_name)

    messages=[]
    messages.append(
        {
        "role": "system",
        "content": template
        }
    )

    user_content="{topic} "+name+" {context} "+text;
    messages.append(
        {
            "role":"user",
            "content": user_content
        }
    )

    #print(messages)

    client=OpenAI()
    
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer=response.choices[0].message.content

    timestamp = int(time.time())
    last2 = timestamp % 100

    suffix = str(last2)
    file_name=name+"_"+suffix+".png"
    answer=answer+"\nfigure.savefig(\""+file_name+"\")"

    answer = answer.replace("figure", "fig" + suffix)\
        .replace("axx", "ax" + suffix)
    
    #print(answer)
    exec(answer)

    return file_name  

def test():
    from dotenv import load_dotenv
    load_dotenv()

    name="atom"
    text="i need a Mind Map for the topic: "+name
    response=generateMindMap_mono_topic(name,text)
    print(response)

    # name="solar system"
    # text="i need a Mind Map for the topic: "+name
    # response=generateMindMap_mono_topic(name,text)
    # print(response)

    # name="atom"
    # text="An atom is the basic unit of matter, consisting of a nucleus at its center, composed of positively charged protons and uncharged neutrons. Negatively charged electrons orbit the nucleus in shells or energy levels. The number of protons in the nucleus determines an element's identity and its chemical properties, while the overall number of electrons balances the positive charge of the protons, making the atom electrically neutral.Atoms are the building blocks of all chemical elements and are crucial to understanding the structure and behavior of matter in the universe."
    # response=generateMindMap_mono_topic(name,text)
    # full_response=response+"\nplt.savefig(\""+name+".png\")"
    # #print(full_response)
    # exec(full_response)

#test()