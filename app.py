import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain_huggingface import ChatHuggingFace
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate

# from langchain_anthropic import ChatAnthropic
# from langchain.chains import RetrievalQA

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInferenceAPIEmbeddings(api_key="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", model_name="sentence-transformers/all-MiniLM-l6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore): 
    llm = ChatOpenAI(model="gpt-4o-mini")
    # llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0.2)
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", task="text-generation",model_kwargs={"temperature":0.8, "max_length":512})
    # llm = HuggingFaceHub(repo_id="google/gemma-7b", task="text-generation", model_kwargs={"temperature":0.5, "max_length":512})
    # llm = HuggingFaceHub(repo_id="meta-llama/Meta-Llama-3-8B-Instruct", task="text-generation", model_kwargs={"temperature":0.1, "max_new_tokens":100,})

    # chat_model = ChatHuggingFace(llm=llm)

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):    
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Iterate over the chat history in the regular order
    for i, message in enumerate(reversed(st.session_state.chat_history)):
        if i % 2 == 0:  # User's message
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:  # Assistant's response
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

            


def main():
    load_dotenv()
    st.set_page_config(page_title="Agribot",page_icon=":corn:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Agribot: Cultivating Knowledge, One Chat at a Time :corn:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
