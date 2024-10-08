"""This class is responsible for ingesting data into the system."""

import logging
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataIngester:
    """Data Ingester class"""

    def __init__(self, config: dict) -> None:
        """
        Initialize the Data Ingester
        
        Args:
            config (dict): The configuration dictionary
        """
        self.config = config
        self.splitter = None
        self.embedder = None
        self.client = None
        self.vector_store = None

    def initialize_embedder(self) -> None:
        """Initialize the embedder"""
        logger.info("Initializing Embedder")
        self.embedder = OpenAIEmbeddings(
            model=self.config["embedder"]["model"],
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        logger.info("Embedder Initialized")

    def initialize_splitter(self) -> None:
        """Initialize the splitter"""
        logger.info("Initializing Splitter")
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config["chunker"]["chunk_size"],
            chunk_overlap=self.config["chunker"]["chunk_overlap"],
            length_function=len,
        )
        logger.info("Splitter Initialized")

    def initialize_vector_store(self) -> None:
        """Initialize the vector store"""
        try:
            logger.info("Initializing Qdrant Vector Store Client")
            self.client = QdrantClient(
                url=os.environ.get("QDRANT_URL"),
                api_key=os.environ.get("QDRANT_API_KEY"),
            )
            logger.info("Qdrant Vector Store Client Initialized")
            logger.info("Creating Collection")
            self.client.create_collection(
                collection_name=self.config["vector_store"]["collection_name"],
                vectors_config=models.VectorParams(
                    size=self.config["vector_store"]["dimension"],
                    distance=self.config["vector_store"]["distance"],
                ),
            )
            logger.info("Collection Created")
        except Exception as e:
            logger.error("Error: %s", e)
            raise e

    def initialize_elements(self) -> None:
        """Initialize the elements"""
        logger.info("Initializing Elements")
        self.initialize_embedder()
        self.initialize_splitter()
        self.initialize_vector_store()
        logger.info("Elements Initialized")

    def ingest_data(self) -> None:
        """Ingesting embeddings data into the vector store"""
        try:
            logger.info("Starting Data Ingestion")
            logger.info("Loading Documents")
            global_chunks = []
            for file in os.listdir(self.config["data"]["raw_path"]):
                if file.endswith(".md"):
                    logger.info("Loading %s", file)
                    file_path = os.path.join(
                        self.config["data"]["raw_path"], file)
                    loader = UnstructuredMarkdownLoader(file_path)
                    documents = loader.load()
                    logger.info("Creating Chunks")
                    chunks = self.splitter.split_documents(documents)
                    global_chunks.extend(chunks)
            logger.info("Ingesting Data")
            self.vector_store = QdrantVectorStore.from_documents(
                url=os.environ.get("QDRANT_URL"),
                api_key=os.environ.get("QDRANT_API_KEY"),
                embedding=self.embedder,
                collection_name=self.config["vector_store"]["collection_name"],
                documents=global_chunks,
                prefer_grpc=True,
            )
            logger.info("Data Ingestestion Completed")
        except Exception as e:
            logger.error("Error: %s", e)
            raise e
