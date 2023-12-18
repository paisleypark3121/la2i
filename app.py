import os
from dotenv import load_dotenv
from typing import Optional

from gtts import gTTS 
from io import BytesIO
import pygame

from typing import List

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import (
    ConversationalRetrievalChain,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.docstore.document import Document
from langchain.memory import ChatMessageHistory, ConversationBufferMemory

from utilities.agent import *
from utilities.MindMapGenerator import *
from utilities.chromadb_manager import *

from openai import OpenAI

import chainlit as cl

save_directory='./files'
persist_directory = 'chroma'
model_name="gpt-3.5-turbo-0613"

system_message="Your role is to be a helpful assistant with a friendly, "\
    "understanding, patient, and user-affirming tone. You should: "\
    "explain topics in short, simple sentences; "\
    "keep explanations to 2 or 3 sentences at most. "\
    "If the user provides affirmative or brief responses, "\
    "take the initiative to continue with relevant information. "\
    "Check for user understanding after each brief explanation "\
    "using varied and friendly-toned questions. "\
    "Use ordered or unordered lists "\
    "(if longer than 2 items, introduce them one by one and "\
    "check for understanding before proceeding), or simple text in replies. "\
    "Provide examples or metaphors if the user doesn't understand. "\
    "Use the following additional [context] below (if present) to retrieve information; "\
    "if you cannot retrieve any information from the [context] use your knowledge. "\
    "[context] {context}"

def setMessages(messages, rolling):
    num_entries = len(messages)
    num_couples = (num_entries - 1) // 2 

    if num_couples <= rolling:
        return messages  
        
    couples_to_remove = num_couples - rolling

    removed_couples = 0
    index = 1  
    while removed_couples < couples_to_remove:
        if messages[index]["role"] == "user" and messages[index + 1]["role"] == "assistant":
            del messages[index]
            del messages[index] 
            removed_couples += 1
        else:
            index += 1

    return messages

rolling = 5

messages=[]
messages.append(
    {
      "role": "system",
      "content": system_message
    }
)

load_dotenv()

@cl.on_chat_start
async def on_chat_start():
    global model_name
    load_dotenv()
    app_user = cl.user_session.get("user")
    if app_user==os.environ.get('LA2I_USERNAME_DSA'):
        model_name=os.environ.get('FINE_TUNED_MODEL')
    #print("START: "+model_name)
    #await cl.Message(f"Hello {app_user.username}").send()

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
    global model_name
    _username=os.environ.get('LA2I_USERNAME')
    _password=os.environ.get('LA2I_PASSWORD')
    _username_dsa=os.environ.get('LA2I_USERNAME_DSA')
    _password_dsa=os.environ.get('LA2I_PASSWORD_DSA')
    if (username.upper(), password) == (_username, _password):
        print("CALL: "+model_name)
        return cl.AppUser(username=_username, role="USER", provider="credentials")
    elif (username.upper(), password) == (_username_dsa, _password_dsa):
        model_name=os.environ.get('FINE_TUNED_MODEL')
        print("CALL: "+model_name)
        return cl.AppUser(username=_username_dsa, role="USER", provider="credentials")
    else:
        return None

@cl.action_callback("Local File")
async def on_action(action):
    global model_name
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a file to begin!",
            accept=["text/plain","application/pdf"],
            max_size_mb=20,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(
        content=f"Processing `{file.name}`...", disable_human_feedback=True
    )
    await msg.send()

    embedding = cl.user_session.get("embedding") 

    #print(type(file))
    if isinstance(file,cl.types.AskFileResponse):
        local_file_name=pre_save_file(file.name,file.content)

    vectordb=create_vectordb_from_file(
        filename=local_file_name,
        persist_directory=persist_directory,
        embedding=embedding,
        overwrite=True,
        chunk_size=500,
        chunk_overlap=50)

    retriever=vectordb.as_retriever()

    # agent=retrieval_agent(
    #     file=local_file_name,
    #     persist_directory=persist_directory,
    #     embedding=embedding,
    #     overwrite=True,
    #     tool_name=file.name,
    #     tool_description=file.name,
    #     model_name=model_name)
    
    #cl.user_session.set("agent", agent)
    #cl.user_session.set("tool", file.name)
    cl.user_session.set("retriever", retriever)

    await cl.Message(content=f"Executed {action.name}").send()

@cl.action_callback("URL")
async def on_action(action):

    content="Insert the URL"
    response = await cl.AskUserMessage(content=content, timeout=30).send()

    if response:
        location=response['content']
        local_file_name=save_file(location=location)
        #print(local_file_name)

        msg = cl.Message(
            content=f"Processing `{os.path.basename(local_file_name)}`...", disable_human_feedback=True
        )
        await msg.send()

        embedding = cl.user_session.get("embedding") 

        # agent=retrieval_agent(
        #     file=local_file_name,
        #     persist_directory=persist_directory,
        #     embedding=embedding,
        #     overwrite=True,
        #     tool_name=os.path.basename(local_file_name),
        #     tool_description=os.path.basename(local_file_name),
        #     model_name=model_name)
        
        # cl.user_session.set("agent", agent)
        # cl.user_session.set("tool", os.path.basename(local_file_name))

        vectordb=create_vectordb_from_file(
            filename=local_file_name,
            persist_directory=persist_directory,
            embedding=embedding,
            overwrite=True,
            chunk_size=500,
            chunk_overlap=50)

        retriever=vectordb.as_retriever()
        cl.user_session.set("retriever", retriever)

        await cl.Message(content=f"Executed {action.name}").send()
        
@cl.action_callback("Text To Speech")
async def on_action(action):
    tts = gTTS(text=action.value, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

@cl.action_callback("Mind Map")
async def on_action(action):
    data = json.loads(action.value)
    name=data["name"]
    text=data["text"]
    
    topic = cl.user_session.get("topic")
    #print("TOPIC: "+topic)
    content="Confirm the topic?"
    if topic!="TODO":
        content+=" ("+topic+")"
    res = await cl.AskUserMessage(content=content, timeout=30).send()
    if res:
        data["name"]=res['content']
        name=data["name"]
        topic=name
        #print(topic)
        cl.user_session.set("topic", topic)
        #response=generateMindMap_context_topic(name,text)
        response=generateMindMap_mono_topic(name,text)
        elements = [
            cl.Image(name=name, display="inline", size="large", path=response)
        ]
        await cl.Message(content=name, elements=elements).send()
        os.remove(response)

@cl.on_chat_start
async def on_chat_start():
    print("CHAT START: "+model_name)
    # Sending an action button within a chatbot message
    app_user = cl.user_session.get("user")
    await cl.Message(f"Hello {app_user.username}").send()
    
    actions = [
        cl.Action(name="Local File", value="load", description="Load Data from File"),
        cl.Action(name="URL", value="load", description="Load Data from URL")
    ]
    await cl.Message(content="Click to Load data", actions=actions).send()

    #await cl.Message(f"This is the model used: {model_name}").send()

    embedding=OpenAIEmbeddings()

    # agent=retrieval_agent(
    #     file=None,
    #     persist_directory=None,
    #     embedding=embedding,
    #     overwrite=True,
    #     tool_name=None,
    #     tool_description=None,
    #     model_name=model_name)
    client=OpenAI()
    
    cl.user_session.set("embedding", embedding)
    #cl.user_session.set("agent", agent)
    cl.user_session.set("client", client)
    cl.user_session.set("messages", messages)
    #cl.user_session.set("retriever", retriever)
    cl.user_session.set("topic", "TODO")

@cl.on_message
async def main(message: cl.Message):

    print("CHAT MAIN: "+model_name)

    # agent = cl.user_session.get("agent")
    # tool = cl.user_session.get("tool")     
    client=cl.user_session.get("client")
    messages=cl.user_session.get("messages")
    retriever=cl.user_session.get("retriever")

    prompt=message.content
    messages.append(
        {
            "role":"user",
            "content": prompt
        }
    )

    if retriever is not None:

        docs=retriever.get_relevant_documents(prompt)
        #print(docs[0])
        updated_system_message=system_message.replace("{context}", docs[0].page_content)

        messages[0]["content"]=updated_system_message
        
    response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0,
                max_tokens=400,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

    answer=response.choices[0].message.content

    messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )
    
    messages=setMessages(messages,rolling)
    cl.user_session.set("messages", messages)

    data = {
        "name": "TODO",
        "text": answer
    }
    json_data = json.dumps(data)

    actions = [
        cl.Action(name="Text To Speech", value=answer, description="Text To Speech"),
        cl.Action(name="Mind Map", value=json_data, description="Mind Map"),
    ]
    await cl.Message(content=answer, actions=actions).send()