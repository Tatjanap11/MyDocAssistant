"""Module to evaluate RAG outputs with RAGAS"""

import logging
import os
from typing import Union

from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
from langchain_openai import OpenAIEmbeddings
from ragas.embeddings.base import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics.base import MetricWithEmbeddings, MetricWithLLM
from ragas.run_config import RunConfig

from src.constants.eval_config import EMBEDDER_MODEL, LLM_MODEL, LLM_TEMPERATURE

logger = logging.getLogger(__name__)


class MetricsEvaluator:
    def __init__(self, metrics: list):
        """
        Initialize the MetricsEvaluator

        Args:
            metrics (list): List of metrics to evaluate
        """
        self.metrics = metrics
        self.llm = None
        self.embedder = None
        self.eval_llm = None
        self.eval_embedder = None

    def _wrap_llm_and_embeddings(
        self, llm: ChatMistralAI, embedder: OpenAIEmbeddings
    ) -> tuple:
        """
        Wrap LLM and Embedder models

        Args:
            llm (ChatMistralAI): The LLM model
            embedder (OpenAIEmbeddings): The Embedder model

        Returns:
            LangchainLLMWrapper, LangchainEmbeddingsWrapper: Wrapped LLM and Embedder models
        """
        logger.info("Wrapping LLM and Embedder models")
        return LangchainLLMWrapper(llm), LangchainEmbeddingsWrapper(embedder)

    def _init_metric(self, metric: Union[MetricWithLLM, MetricWithEmbeddings]) -> None:
        """
        Initialize a metric

        Args:
            metric (Union[MetricWithLLM, MetricWithEmbeddings]): The metric to initialize
        """
        logger.info("Initializing metric: %s", metric.name)
        if isinstance(metric, MetricWithLLM):
            logger.info("Setting LLM for metric: %s", metric.name)
            metric.llm = self.llm
        if isinstance(metric, MetricWithEmbeddings):
            logger.info("Setting Embeddings for metric: %s", metric.name)
            metric.embeddings = self.embedder
        run_config = RunConfig()
        metric.init(run_config)

    def init_models(self) -> None:
        """
        Initialize the LLM and Embedder models for evaluation
        """
        logger.info("Initializing LLM and Embedder models")
        if("llama" in LLM_MODEL):
            self.eval_llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            api_key=os.environ["GROQ_API_KEY"],
        )
        else:
            self.eval_llm = ChatMistralAI(
                model=LLM_MODEL,
                temperature=LLM_TEMPERATURE,
                api_key=os.environ["MISTRAL_API_KEY"],
            )
        self.eval_embedder = OpenAIEmbeddings(
            model=EMBEDDER_MODEL, api_key=os.environ["OPENAI_API_KEY"]
        )

        self.llm, self.embedder = self._wrap_llm_and_embeddings(
            self.eval_llm, self.eval_embedder
        )

    def init_metrics(self) -> None:
        """
        Initialize the metrics for evaluation
        """
        logger.info("Initializing metrics")
        for metric in self.metrics:
            self._init_metric(metric)
        logger.info("Metrics initialized successfully")

    def calculate_scores(self, question:str, context:list, answer:str) -> dict:
        """
        Method to calculate RAGAS scores

        Args:
            question (str): The question
            context (list): The context
            answer (str): The answer

        Returns:
            dict: The scores
        """
        logger.info("Calculating RAGAS scores")

        scores = {
            metric.name: metric.score(
                {"question": question, "contexts": context, "answer": answer}
            )
            for metric in self.metrics
        }

        logger.info("Scores calculated: %s", scores)
        return scores
