# MyDocAssistant
MyDocAssistant is a proof of concept (POC) tool designed to help developers efficiently navigate AWS documentation. This tool reduces the time spent searching for information by leveraging natural language processing (NLP) techniques to understand developer queries and retrieve relevant answers from indexed documentation.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)

## Features

- Ingest various document formats and extract relevant information.
- Evaluate the quality and relevance of documents using built-in evaluation metrics.
- Generate insights and summaries based on document contents.
- Easily configurable through a YAML configuration file.

## Installation

1. Clone the repository:
```bash
git clone https://<user>:<public_token>@github.com/yourusername/MyDocAssistant.git
cd MyDocAssistant
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate 
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Configure environment variables by copying the example:
```bash
cp .env.example .env
```
5. Update the .env file with your specific configurations.

## Usage

1.  To perform data ingestion in vector store, execute the following command:
```bash
python src/workflows/ingestion_workflows.py
 ```
2. To run inference and calculate scores, execute the following command:
```bash
python src/workflows/inference_workflows.py
 ```
3. To analyse and compare experiments use mlflow by running the command in the current directory
```bash
mlflow ui
 ```

> [!NOTE]
> Make sure that the path to configuration_llama.yaml or configuration_mistral.yaml and any other resources used in the DataIngester class and RAG class are correct and that the required files are present in the specified directories, as well as provide the path to the configuration files before running the workflows. For evaluation the eval_config.py parameters should also be set correctly.



## Directory Structure

```bash
MyDocAssistant
├── configs
│   └── configuration.yaml          # Configuration file for the application
├── data
│   └── sagemaker_documentation     # Documentation files for SageMaker integration
├── src
│   ├── constants                   # Constants and prompt definitions
│   │   ├── eval_config.py
│   │   ├── prompt.py
│   │   └── questions.py
│   ├── models                      # Machine learning models and data processing
│   │   ├── data_ingester.py
│   │   └── rag.py
│   ├── utils                       # Utility functions
│   │   ├── evaluation.py
│   │   └── load_configuration.py
│   └── workflows                   # Workflow definitions
│       ├── inference_workflows.py
│       └── ingestion_workflows.py
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore file
├── README.md                       # This README file
├── requirements.txt                # Project dependencies
└── Senior_ML_Tech_Assessment.pdf   # Assessment document for review
```


#Detailed explanation

## Key Project Objectives

- **Efficient Search**: Enables developers to quickly find relevant information in AWS Sagemaker documentation, minimizing time spent manually browsing.
- **Up-to-Date Information**: Provides current information from AWS Sagemaker documentation, with plans to integrate internal documentation updates in later stages.
- **Traceability**: Each search result includes the exact source of information.
- **Sensitive Data Compliance**: Supports compliance with external sharing restrictions and geographical limitations for handling sensitive information.

Built on a Retrieval Augmented Generation (RAG) system, this solution retrieves relevant documentation sections and generates coherent answers based on provided AWS Sagemaker documentation. The current vector database, **Qdrant**, operates in the EU-East region (with an optional US-based plan available).

## Project Components and Patterns

### Retrieval Augmented Generation (RAG) Pattern

The RAG-based approach includes:

1. **Retrieval Component**: Retrieves relevant document sections from a vector store, ensuring contextually relevant and updated information for each query.
2. **Generation Component**: Generates detailed, coherent responses tailored to the query by synthesizing retrieved data.

This pattern supports efficient handling of extensive documentation, optimizing accuracy, and reducing reliance on outdated or irrelevant information.

## Tools and Frameworks

- **LangChain**: Used for data loading, splitting, embedding management, and vector store initialization. Simplifies integration of large language models and RetrievalQA.
- **Qdrant**: High-performance vector store for managing and searching embeddings, enabling efficient document retrieval.
- **API Providers**: Integration with OpenAI, Groq, and Mistral APIs for advanced model access.
- **Ragas**: Tool for system performance evaluation using retrieval and generation metrics.
- **MLflow**: Tracks model parameters, metrics, and artifacts to monitor and compare model performance over time.

## Model Selection

For optimal balance between speed and performance, **Llama-3.1-8B** and **Mixtral-7x8B** models were selected:

- **Performance**: Both models provide coherent, relevant responses, optimizing retrieval effectiveness.
- **Speed**: Compact model sizes facilitate faster processing, crucial for real-time applications.

Detailed results from model experimentation can be found in the `MLflow` logs.

### Embedding Model Selection

The **text-embedding-ada-002** model was chosen for generating embeddings, striking a balance of size and performance. This model optimizes tasks like text search and similarity with minimal computational overhead.

## Handling Out-of-Vocabulary (OOV) Terms

The system addresses OOV terms through contextual embeddings from the **text-embedding-ada-002** model, along with **Qdrant** for retrieval:

- **Contextual Embeddings**: Allows inference of OOV terms by capturing nuances from surrounding words.
- **Vector Store Retrieval**: Finds semantically similar terms to generate context-aligned responses.
- **Continuous Learning**: Potential to ingest new data progressively, enhancing vocabulary and adaptability.

## Self-Hosting and Deployment Considerations

While self-hosting is not required for this POC, **Qdrant** supports regional selection within the U.S., meeting data compliance needs for internal documentation. The project is currently run locally with embedding and LLM APIs accessed remotely, with potential for Docker-based cloud deployment in future stages.

## Document Chunking

Documents were segmented using **Langchain’s RecursiveCharacterTextSplitter** to balance context preservation and processing efficiency. Experiments showed improvements in chunking performance with adjustments to chunk size and overlap, refined with **ChunkViz** for optimal results.

## Production-Readiness Enhancements

To ensure production readiness:

- Additional testing with larger datasets to identify the best embeddings and LLM combinations.
- Cloud deployment with Docker and an enhanced user interface (UI) for improved user experience.
- Regularly updating embeddings and vector store content to ensure responses remain accurate with documentation changes.

## Adaptation to Changing Information

Currently, the system does not handle changes in documentation automatically. However, updates can be managed by refreshing the vector store with new embeddings, potentially adding a document check mechanism to identify updates and new content.

## System Evaluation

The **RAGAS** framework was used to evaluate the system using the following key metrics:

1. **Faithfulness**: Measures how well the answer aligns with the provided context (scaled 0-1).
2. **Answer Relevancy**: Assesses relevance to the prompt using cosine similarity.
3. **Context Utilization**: Evaluates the effectiveness of retrieval based on answer relevance.

### Information Retrieval Evaluation

**Context utilization** metric measures retrieval precision by evaluating if answer-relevant items rank higher in retrieval, with higher scores indicating better precision.

### Production Evaluation Considerations

For production, larger datasets with ground truth data are necessary to benchmark performance in real-world scenarios, providing a more robust system validation.

---

For more details, see the experiment logs in `MLflow` and refer to the `experiments` folder.
