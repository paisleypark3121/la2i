from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
import json

import networkx as nx
import matplotlib.pyplot as plt
#from networkx.drawing.nx_pydot import graphviz_layout
from networkx.drawing.nx_agraph import graphviz_layout

system_message_mono_topic = "You are a helpful assistant that generates "\
    "a coded Mind Map or Conceptual Map given a base topic. "\
    "Each map has to contain a maximum of 3 concepts and all connections must be labelled."\
    "The output has to be the CODE to be used in NetworkX in order to have the map done; "\
    "this output has to contain ONLY the code needed without any import."\
    "As an example, the output has to start with '''G = nx.Graph();"\
    "For example if the user asks for the topic: atom, you need to provide as output: "\
    '''G = nx.Graph()
G.add_node("Atomo", label="Atomo")
G.add_node("Nucleo", label="Nucleo")
G.add_node("Protoni", label="Protoni")
G.add_node("Neutroni", label="Neutroni")
G.add_node("Elettroni", label="Elettroni")
G.add_edge("Atomo", "Nucleo")
G.add_edge("Nucleo", "Protoni")
G.add_edge("Nucleo", "Neutroni")
G.add_edge("Atomo", "Elettroni")
node_labels = nx.get_node_attributes(G, 'label')
node_sizes = [len(label) * 200 for label in node_labels]
pos = graphviz_layout(G, prog="dot")
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=8, edge_color="gray", arrowsize=20)
plt.savefig("atom.png")'''

system_message_context_topic = "You are a helpful assistant that generates "\
    "a coded Mind Map or Conceptual Map given a [context] of information on a base [topic]. "\
    "Each map has to contain a maximum of 5 concepts and all connections must be labelled."\
    "The output has to be the CODE to be used in NetworkX in order to have the map done; "\
    "this output has to contain ONLY the code needed without any import."\
    "As an example, the output has to start with "\
    "G = nx.Graph(); "\
    "has to finish with "\
    "plt.savefig([topic]) "\
    "the instructions in the middle must contain nodes and labels according to the given [context]."\
    "An output example could be: "\
    '''G = nx.Graph()
G.add_node("Atomo", label="Atomo")
G.add_node("Nucleo", label="Nucleo")
G.add_node("Protoni", label="Protoni")
G.add_node("Neutroni", label="Neutroni")
G.add_node("Elettroni", label="Elettroni")
G.add_edge("Atomo", "Nucleo")
G.add_edge("Nucleo", "Protoni")
G.add_edge("Nucleo", "Neutroni")
G.add_edge("Atomo", "Elettroni")
node_labels = nx.get_node_attributes(G, 'label')
node_sizes = [len(label) * 200 for label in node_labels]
pos = graphviz_layout(G, prog="dot")
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=8, edge_color="gray", arrows=True, arrowsize=20)
plt.savefig("atom.png")'''

template = """You are a helpful assistant that generates a coded Mind Map given a specific [topic] and a [context].
Each map has to contain a maximum of 3 concepts and all connections must be labelled.
The output has to be the NetworkX python code needed to produce the mind map. This output has to contain only the code needed without any import.
As an example, the output has to start with: 
G = nx.Graph(); 
As an example, if the user asks for: 
[topic] atom
[context] An atom is the fundamental building block of matter, consisting of two main components: electrons and nucleus. Electrons are negatively charged subatomic particles that orbit the nucleus in specific energy levels or electron shells; the nucleus is the central, densely packed core of an atom, where most of its mass is concentrated and contains two types of particles: protons (positively charged subatomic particles) and neutrons (electrically neutral subatomic particles).

coded mind map:
G = nx.Graph()
G.add_node("atom", label="atom")
G.add_node("nucleus", label="nucleus")
G.add_node("protons", label="protons")
G.add_node("neutrons", label="neutrons")
G.add_node("electrons", label="electrons")
G.add_edge("atom", "nucleus", label="composition")
G.add_edge("nucleus", "protons", label="compositions")
G.add_edge("nucleus", "neutrons", label="composition")
G.add_edge("atom", "electrons", label="composition")
pos = graphviz_layout(G, prog="dot")
node_labels = nx.get_node_attributes(G, 'label')
node_sizes = [len(label) * 200 for label in node_labels]
edge_labels = dict()
for edge in G.edges():
    node1, node2 = edge
    edge_labels[edge] = G[node1][node2]['label']
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=node_sizes, node_color="skyblue", font_size=8, edge_color="gray", arrows=True, arrowsize=20)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='red')'''
[topic]{topic}
[context]{context}

coded mind map:"""

    
#def generateMindMap_mono_topic(name,text,temperature=0,model_name='gpt-3.5-turbo-0613'):
def generateMindMap_mono_topic_old(name,text,temperature=0,model_name='gpt-4-0613'):

    llm = ChatOpenAI(
        temperature=temperature,
        model_name=model_name
    )

    response=llm(
        [
            SystemMessage(content=system_message_mono_topic),
            HumanMessage(content=text)
        ]
    )
    exec(response.content)
    print(response.content)
    print(name)
    return name.replace(" ", "_")+".png"

def generateMindMap_mono_topic(name,text,temperature=0,model_name='gpt-4-0613'):
#def generateMindMap_mono_topic(name,text,temperature=0,model_name='gpt-3.5-turbo-1106'):

    llm = ChatOpenAI(
        temperature=temperature,
        model_name=model_name
    )

    prompt = PromptTemplate.from_template(
        template
    )
    prompt.format(topic=name, context=text)
    
    llm_chain = LLMChain(
        llm=llm, 
        prompt=prompt)

    response=llm_chain.invoke({"topic":name,"context":text})
    file_name=name+".png"
    full_response=response["text"]+"\nplt.savefig(\""+file_name+"\")"
    exec(full_response)
    return file_name
    #return response['text']
    #print(response.text)
    # exec(response.content)
    # print(response.content)
    # print(name)
    # return name.replace(" ", "_")+".png"

#def generateMindMap_context_topic(name,text,temperature=0,model_name='gpt-3.5-turbo-0613'):
def generateMindMap_context_topic(name,text,temperature=0,model_name='gpt-4-0613'):

    llm = ChatOpenAI(
        temperature=temperature,
        model_name=model_name
    )

    messages=[
        SystemMessage(content=system_message_context_topic),
    ]

    prompt = HumanMessage(
        content=human_message_template.format(topic=name, context=text)
    )
    messages.append(prompt)

    response=llm(messages)
    exec(response.content)
    return "./"+name.replace(" ", "_")+".png"
    
def test():
    from dotenv import load_dotenv
    load_dotenv()

    # name="atom"
    # text="i need a Mind Map for the topic: "+name
    # response=generateMindMap_mono_topic(name,text)
    # print(response)

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

test()