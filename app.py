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

import chainlit as cl

save_directory='./files'
persist_directory = 'chroma'

load_dotenv()

@cl.on_chat_start
async def on_chat_start():
    load_dotenv()
    app_user = cl.user_session.get("user")
    await cl.Message(f"Hello {app_user.username}").send()

@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
    _username=os.environ.get('LA2I_USERNAME')
    _password=os.environ.get('LA2I_PASSWORD')
    if (username.upper(), password) == (_username, _password):
        return cl.AppUser(username=_username, role="USER", provider="credentials")
    else:
        return None

@cl.action_callback("Local File")
async def on_action(action):

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

    agent=retrieval_agent(
        file=local_file_name,
        persist_directory=persist_directory,
        embedding=embedding,
        overwrite=True,
        tool_name=file.name,
        tool_description=file.name)
    
    cl.user_session.set("agent", agent)
    cl.user_session.set("tool", file.name)

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

        agent=retrieval_agent(
            file=local_file_name,
            persist_directory=persist_directory,
            embedding=embedding,
            overwrite=True,
            tool_name=os.path.basename(local_file_name),
            tool_description=os.path.basename(local_file_name))
        
        cl.user_session.set("agent", agent)
        cl.user_session.set("tool", os.path.basename(local_file_name))

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
        print(topic)
        cl.user_session.set("topic", topic)
        #response=generateMindMap_context_topic(name,text)
        response=generateMindMap_mono_topic(name,text)
        elements = [
            cl.Image(name=name, display="inline", path=response)
        ]
        await cl.Message(content=name, elements=elements).send()
        os.remove(response)

@cl.on_chat_start
async def on_chat_start():
    # Sending an action button within a chatbot message
    actions = [
        cl.Action(name="Local File", value="load", description="Load Data from File"),
        cl.Action(name="URL", value="load", description="Load Data from URL")
    ]

    await cl.Message(content="Click to Load data", actions=actions).send()

    embedding=OpenAIEmbeddings()

    agent=retrieval_agent(
        file=None,
        persist_directory=None,
        embedding=embedding,
        overwrite=True,
        tool_name=None,
        tool_description=None)
    
    cl.user_session.set("embedding", embedding)
    cl.user_session.set("agent", agent)
    cl.user_session.set("topic", "TODO")

@cl.on_message
async def main(message: cl.Message):

    agent = cl.user_session.get("agent")
    tool = cl.user_session.get("tool")     

    # print("***")
    # print(agent.memory.buffer)
    # print(message.content)
    # print("***")

    if agent is not None:

        answer_prefix_tokens=["FINAL", "ANSWER"]

        prompt=message.content
        if tool:
            prompt="Please use the tool "+tool+" to produce the output for the user request: "+message.content
            
        response = await agent.acall(
            prompt, 
            callbacks=[cl.AsyncLangchainCallbackHandler(
                stream_final_answer=True,
                answer_prefix_tokens=answer_prefix_tokens
            )])

        answer = response["output"]

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

    # source_documents = res["source_documents"]  # type: List[Document]

    # text_elements = []  # type: List[cl.Text]

    # if source_documents:
    #     for source_idx, source_doc in enumerate(source_documents):
    #         source_name = f"source_{source_idx}"
    #         # Create the text element referenced in the message
    #         text_elements.append(
    #             cl.Text(content=source_doc.page_content, name=source_name)
    #         )
    #     source_names = [text_el.name for text_el in text_elements]

    #     if source_names:
    #         answer += f"\nSources: {', '.join(source_names)}"
    #     else:
    #         answer += "\nNo sources found"

    #await cl.Message(content=answer, elements=text_elements).send()

    # chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    # cb = cl.AsyncLangchainCallbackHandler()

    # res = await chain.acall(message.content, callbacks=[cb])
    # answer = res["answer"]
    # source_documents = res["source_documents"]  # type: List[Document]

    # text_elements = []  # type: List[cl.Text]

    # if source_documents:
    #     for source_idx, source_doc in enumerate(source_documents):
    #         source_name = f"source_{source_idx}"
    #         # Create the text element referenced in the message
    #         text_elements.append(
    #             cl.Text(content=source_doc.page_content, name=source_name)
    #         )
    #     source_names = [text_el.name for text_el in text_elements]

    #     if source_names:
    #         answer += f"\nSources: {', '.join(source_names)}"
    #     else:
    #         answer += "\nNo sources found"

    # await cl.Message(content=answer, elements=text_elements).send()