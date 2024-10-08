"""Inference pipeline for the RAG."""

import logging

import mlflow
import pandas as pd
from dotenv import load_dotenv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# import src
from src.constants.eval_config import METRICS
from src.constants.prompt import LLAMA_3_PROMPT, SYSTEM_MESSAGE, USER_MESSAGE
from src.constants.questions import QUESTIONS
from src.models.rag import RAG
from src.utils.evaluation import MetricsEvaluator
from src.utils.load_configuration import load_yaml_configuration

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    config_path = r"C:\Users\tatja\Desktop\RAGTask\Code\LokaDocAssistant/configs/configuration.yaml"
    template = LLAMA_3_PROMPT
    system_message = SYSTEM_MESSAGE
    user_message = USER_MESSAGE
    metric_names = [metric.name for metric in METRICS]
    column_names = ["question", "context", "answer"].extend(metric_names)
    config = load_yaml_configuration(config_path)
    mlflow.set_experiment(config["experiment_name"])

    # Start MLflow run
    with mlflow.start_run():
        mlflow.langchain.autolog(log_traces=True)
        mlflow.log_params(config)
        mlflow.log_params(
            {"model_type": "RAG", "config_path": "configs/configuration.yaml"}
        )
        mlflow.log_params(
            {
                "prompt_template": template,
                "system_message": system_message,
                "user_message": user_message,
            }
        )
        mlflow.log_artifact(config_path)

        # Initialize RAG model
        rag_model = RAG(config=config)
        rag_model.initialize_elements()  # Initialize all components

        rag_model.prompt_template(
            template=template, system_message=system_message, user_message=user_message
        )


        logger.info("Running inference")
        rag_model.retriever_qa_chain()

        logger.info("Initializing LLM and metrics for evaluation")
        evaluator = MetricsEvaluator(METRICS)
        evaluator.init_models()  # Initialize models
        evaluator.init_metrics()  # Initialize metrics

        eval_df = pd.DataFrame(columns=column_names)

        for question in QUESTIONS:
            contexts = rag_model.retriever.invoke(question)
            answer = rag_model.chain.invoke(
                {
                    "query": question,
                    "context": contexts,
                }
            )["result"]

            # Log the response
            logger.info("Answer for given questions %s is %s", question, answer)

            contexts_content = [
                context.page_content for context in contexts
            ]

            scores = evaluator.calculate_scores(question, contexts_content, answer)
            output_row = {
                "question": question,
                "context": contexts_content,
                "answer": answer,
                **scores,
            }

            eval_df = pd.concat([eval_df, pd.DataFrame([output_row])], ignore_index=True)

        logger.info("Evaluation completed")
        eval_df.to_csv("evaluation_results.csv")


if __name__ == "__main__":
    main()
