"""Evaluation configuration for the RAG"""

from ragas.metrics import (
    answer_relevancy,
    context_utilization,
    faithfulness,
)

LLM_MODEL = "mistral-large-latest"
LLM_TEMPERATURE = 0.2
EMBEDDER_MODEL = "text-embedding-ada-002"
METRICS = [faithfulness, answer_relevancy, context_utilization]
