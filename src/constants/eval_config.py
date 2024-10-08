"""Evaluation configuration for the RAG"""

from ragas.metrics import (
    answer_relevancy,
    context_utilization,
    faithfulness,
)

LLM_MODEL = "llama3-70b-8192"
LLM_TEMPERATURE = 0
EMBEDDER_MODEL = "text-embedding-ada-002"
METRICS = [faithfulness, answer_relevancy, context_utilization]
