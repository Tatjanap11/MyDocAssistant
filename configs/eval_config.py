from ragas.metrics import answer_relevancy,answer_correctness, context_utilization, faithfulness,context_precision,context_recall

LLM_MODEL = "mistral-large-latest"
LLM_MAX_TOKENS = None
LLM_TEMPERATURE = 0

# Constants for embedder configuration
EMBEDDER_MODEL = "text-embedding-ada-002"
METRICS=[faithfulness,answer_relevancy,context_utilization]