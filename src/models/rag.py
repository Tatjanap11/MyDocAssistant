"""This class is responsible for creating the RAG model."""

import logging
import os

from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAG:
    """RAG model class"""

    def __init__(self, config: dict) -> None:
        """
        Initialize the RAG model.

        Args:
            config (dict): The configuration dictionary

        """
        self.config = config
        self.llm = None
        self.embedder = None
        self.vector_store = None
        self.retriever = None
        self.chain = None
        self.prompt = None

    def initialize_llm(self) -> None:
        """
        Method to initialize the LLM.
        """
        logger.info("Initializing LLM")

        self.llm = ChatGroq(
            model_name=self.config["llm"]["model"],
            temperature=self.config["llm"]["temperature"],
            max_tokens=self.config["llm"]["max_tokens"],
            groq_api_key=os.environ["GROQ_API_KEY"],
        )
        logger.info("LLM initialized")

    def initialize_embedder(self) -> None:
        """Initialize the embedder"""
        logger.info("Initializing Embedder")
        self.embedder = OpenAIEmbeddings(
            model=self.config["embedder"]["model"],
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        logger.info("Embedder Initialized")

    def initialize_vector_store(self) -> None:
        """Initialize the vector store"""
        try:
            logger.info("Initializing Qdrant Vector Store Client")
            self.vector_store = QdrantVectorStore.from_existing_collection(
                url=os.environ.get("QDRANT_URL"),
                api_key=os.environ.get("QDRANT_API_KEY"),
                embedding=self.embedder,
                collection_name=self.config["vector_store"]["collection_name"],
            )
        except Exception as e:
            logger.error("Error: %s", e)
            raise e

    def initialize_retriever(self) -> None:
        """
        Method to initialize the retriever.
        """
        logger.info("Initializing retriever")
        self.retriever = self.vector_store.as_retriever(
            search_type=self.config["retriever"]["search_type"],
            retriever_kwargs=self.config["retriever"]["retriever_kwargs"],
        )
        logger.info("Retriever initialized")

    def initialize_elements(self) -> None:
        """Initialize the elements"""
        logger.info("Initializing Elements")
        self.initialize_llm()
        self.initialize_embedder()
        self.initialize_vector_store()
        self.initialize_retriever()
        logger.info("Elements Initialized")

    def prompt_template(
        self, template: str, system_message: str, user_message: str
    ) -> None:
        """
        Method to create the prompt for the LLM.

        Args:
            template (str): The template for the prompt
            system_message (str): The system message
            user_message (str): The user message
        """

        logger.info("Creating prompt")
        template = template.format(
            system_message=system_message,
            user_message=user_message,
        )
        self.prompt = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )
        logger.info("Prompt created")

    def retriever_qa_chain(self):
        """Method to get the retrieval QA chain."""
        logger.info("Creating retrieval QA chain")
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type_kwargs={"prompt": self.prompt, "verbose": True},
        )
        logger.info("Retrieval QA chain created")

        return self.chain
