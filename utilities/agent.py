from utilities.chromadb_manager import *

from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings

from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate

from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.prompts import MessagesPlaceholder

from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
    AgentTokenBufferMemory,
)


from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

from langchain.memory import ConversationBufferWindowMemory

from langchain.agents import (
    AgentExecutor,
    AgentType,
    initialize_agent,
    Tool
)

from langchain.agents.agent_toolkits import (
    create_retriever_tool,
    create_conversational_retrieval_agent
)

from langchain.chains import ConversationalRetrievalChain

def retrieval_agent(
    file,
    persist_directory,
    embedding,
    overwrite,
    tool_name,
    tool_description,
    #model_name="gpt-3.5-turbo",
    #model_name="gpt-3.5-turbo-0613",
    #model_name="gpt-4-0613",
    model_name="gpt-3.5-turbo-1106",
    temperature=0,
    k=3,
    language_code="it"):

    retriever = None
    if file is not None:

        local_file=save_file(
            location=file,
            language_code=language_code
        )

        vectordb=create_vectordb_from_file(
            filename=local_file,
            persist_directory=persist_directory,
            embedding=embedding,
            overwrite=overwrite
        )

        retriever = vectordb.as_retriever()

    conversational_memory = ConversationBufferWindowMemory(
        memory_key="chat_history", #needs to be present
        ai_prefix="AI Assistant",
        k=k, #how many interactions can be remembered
        return_messages=True
    )

    print("RETRIEVAL: "+model_name)
    llm=ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        streaming=True
    )

    if retriever:
        qa=RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff", 
            retriever=retriever
        )

        tools = [
            Tool(
                #name="jokerbirot story",
                name=tool_name,
                func=qa.run,
                #description="use this tool when answering questions about the topic" #the description is important because the agent, based on this will decide which tool to use
                description=tool_description
            )
        ]

        agent=initialize_agent(
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, #https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html#langchain.agents.agent_types.AgentType
            llm=llm,
            tools=tools,
            memory=conversational_memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=k, #caps the agent at taking a certain number of steps
            early_stopping_method="generate", #By default, the early stopping uses the force method which just returns that constant string. Alternatively, you could specify the generate method which then does one FINAL pass through the LLM to generate an output
        )

        return agent
    else:
        agent=initialize_agent(
            tools=[],
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, #https://api.python.langchain.com/en/latest/agents/langchain.agents.agent_types.AgentType.html#langchain.agents.agent_types.AgentType
            llm=llm,
            memory=conversational_memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=k, #caps the agent at taking a certain number of steps
            early_stopping_method="generate", #By default, the early stopping uses the force method which just returns that constant string. Alternatively, you could specify the generate method which then does one FINAL pass through the LLM to generate an output
        )

        return agent