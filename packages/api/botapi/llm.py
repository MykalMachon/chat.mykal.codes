from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import requests

context = """
You are a chatbot called mykal.ai. 
The content you're aware of is from a blog called mykal.codes, written and owned by Mykal Machon.
Your goal is to summarize, share, and provide links to content on this blog. 
You are to do this while being kind and with a great attitude. 
"""

# TODO: look into using a ConversationalRetrievalChain to enable actual conversation
# here is a link for more information on this approach
# https://python.langchain.com/docs/use_cases/chatbots#chat-retrieval

MODEL_FOLDER = Path("/srv/chat")


def get_model():
    """Ingests data from the main feed and loads it into the model"""
    print("getting model...")
    # check if /srv/chat folder exists, make new folder if not
    if not MODEL_FOLDER.exists():
        print("could not find model folder, creating new folder...")
        MODEL_FOLDER.mkdir()

    # check if model file store.index and faiss_store.pkl exists
    if (
        not Path(f"{MODEL_FOLDER}/docs.index").exists()
        or not Path(f"{MODEL_FOLDER}/faiss_store.pkl").exists()
    ):
        print("could not find model, creating new model...")
        ingest_data_into_model()
        return load_existing_model()
    else:
        print("found model on disk, loading existing model...")
        return load_existing_model()


def load_existing_model():
    """Loads a model from the disk"""
    index = faiss.read_index(f"{MODEL_FOLDER}/docs.index")
    with open(f"{MODEL_FOLDER}/faiss_store.pkl", "rb") as f:
        store = pickle.load(f)

    store.index = index
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        return_source_documents=True,
        retriever=store.as_retriever(),
    )
    return chain


def ingest_data_into_model():
    """Ingests data from the main feed and loads it into the model"""
    json_posts = requests.get("https://mykal.codes/feeds/main.json").json()

    data = []
    sources = []

    for post in json_posts:
        data.append(post["body"])
        sources.append(f"https://mykal.codes/{post['collection']}/{post['slug']}")

    # split data into chunks
    splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
    docs = []
    metadata = []
    for i, d in enumerate(data):
        splits = splitter.split_text(d)
        docs.extend(splits)
        metadata.extend([{"source": sources[i]}] * len(splits))

    # vectorize data
    store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadata)
    faiss.write_index(store.index, f"{MODEL_FOLDER}/docs.index")
    with open(f"{MODEL_FOLDER}/faiss_store.pkl", "wb") as f:
        pickle.dump(store, f)


if __name__ == "__main__":
    model = get_model()
    result = model({"question": "What do you know about Coffee?"})
    print(result)
