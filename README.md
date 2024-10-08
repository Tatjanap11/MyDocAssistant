# LokaDocAssistant
LokaDocAssistant is a proof of concept (POC) tool designed to help developers efficiently navigate AWS documentation. This tool reduces the time spent searching for information by leveraging natural language processing (NLP) techniques to understand developer queries and retrieve relevant answers from indexed documentation.

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
git clone https://<user>:<public_token>@github.com/yourusername/LokaDocAssistant.git
cd LokaDocAssistant
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

> [!NOTE]
> Make sure that the path to configuration.yaml and any other resources used in the DataIngester class and RAG class are correct and that the required files are present in the specified directories. For evaluation the eval_config.py parameters should also be set correctly.

## Directory Structure

```bash
LokaDocAssistant
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
# # Answers to suggested questions

### 1. **Does your solution solve the company’s pain points? What are they?**

**Answer**:  
Main key points from Company X were:

•	Development of a system to assist developers in searching through AWS Sagemaker documentation (initially, a small subset was provided).

•	The system must deliver fast search results, minimizing the need to manually browse through documentation.

•	It should always provide up-to-date information from AWS Sagemaker documentation, and in later stages, from internal documentation as well.

•	The system should indicate the exact source of information for each result.

•	It must handle sensitive, proprietary information, ensuring compliance with external sharing restrictions and geographical limitations.

The proposed system is designed to address all requirements from Company X. The RAG(Retrieval Augmented Generation) system is built on the AWS Sagemaker documentation, specifically focusing on a provided subset. It effectively retrieves relevant information and generates trustworthy and reliable answers to user queries. It also identifies the source of the information from which the answers are derived. However, it currently lacks the capability to consistently access the latest updates from the AWS Sagemaker documentation, as well as internal documentation in future iterations. This can be resolved by implementing a mechanism to check if a document is new or if there have been updates to an existing document and updating the vector database with new content, including internal documents. The vector database used in the POC is Qdrant, which can be configured to enforce geographical restrictions. For the proof of concept, it is set to the EU-East region, but there is a paid plan($0.03566/h) available that can be configured to operate in the US.


---

### 2. **What is the name of the LLM Pattern you’ve used in this project?**  
Since names are not yet standardized, feel free to elaborate on the pattern you used.

**Answer**:  
As mentioned in answer 1, I used a RAG system as POC to build a tool for searching through large amount of documentation.
Here's a brief elaboration on the pattern:

Retrieval Component: The system first retrieves relevant documents or chunks from a vector store based on the user’s query. This ensures that the information used for generating answers is contextually relevant and up-to-date.

Generation Component: After retrieving relevant information, a language model (ex. Llama3-8B) generates responses by synthesizing the retrieved data. This step allows the system to provide detailed, coherent answers that are tailored to the specific query.

Benefits: By integrating retrieval and generation, RAG allows for handling large volumes of documentation effectively, improving the accuracy of responses, and reducing the reliance on outdated or irrelevant information. This pattern is particularly suitable for use cases involving extensive documentation, such as the AWS documentation provided for this proof of concept, while also being adaptable for future integration of internal, sensitive documents.

---

### 3. **What tools did you use? Why did you select them?**

**Answer**:  

In this project, I utilized a variety of tools to enhance the functionality and performance of the solution:

•	LangChain: I selected this framework for its capabilities in loading and splitting data, managing the embeddings model, and initializing and ingesting data into the vector store. It also facilitated the implementation of LLM models and the RetrievalQA chain. LangChain streamlines the integration of various modules, making the application easier to build and maintain.

•	Qdrant: I chose Qdrant as the vector store due to its high-performance capabilities in managing and searching through extensive sets of embeddings. Its design supports real-time vector similarity searches, which are essential for efficiently retrieving relevant documents based on user queries.

•	OpenAI, Groq, and Mistral as API providers to generate keys in order to use the wrappers in LangChain which enables  seamless access to advanced models.

•	Ragas: I employed Ragas to evaluate the system's performance, leveraging its comprehensive suite of metrics for assessing information retrieval and generation tasks. This tool allows for thorough evaluation of the accuracy and relevance of the model's responses.

•	MLflow: I integrated MLflow to track experiments and ensure reproducibility. This platform enables the logging of model parameters, metrics, and artifacts, facilitating easier monitoring of model performance over time and comparisons between different runs.


---

### 4. **What model would you use for this use case? Why?**

**Answer**:  
For this use case, I experimented with the llama-3.1-8b and Mixtral-7x8B models, focusing on their size and performance:

•	Size and Speed: Both models are compact, allowing for faster processing—essential for real-time applications.

•	Performance: They deliver coherent and relevant responses, significantly enhancing the system's ability to retrieve information effectively.

•	Open-source and free

The Llama-3.1-8B and Mixtral-7x8B models strike an excellent balance between speed and effectiveness, making them ideal for this proof of concept. Notably, Mixtral outperformed Llama in the experiments, and detailed results can be found in the experiments folder or in the MLflow runs.


#### (a) **What did you use for your embeddings? How does that decision affect the performance of your system?**

**Answer**:
I used text-embedding-ada-002 for generating embeddings. The main reasoning is that it is considered a small model compared to larger models like Davinci. Its design focuses on providing high performance in tasks such as text and code search, text similarity, and more, while maintaining a smaller size and lower resource requirements. This smaller model size allows for faster inference times and easier integration into applications without the computational overhead.

---

### 5. **How does your system handle out-of-vocabulary (OOV) terms?**

**Answer**:  
The system could handle out-of-vocabulary (OOV) terms by utilizing embeddings generated from “text-embedding-ada-002” model alongside the Qdrant vector store:

•	Contextual Embeddings: OOV terms are processed through embeddings that capture the nuances of surrounding words, enabling the model to infer meanings even in the absence of specific vocabulary.

•	Vector Store Retrieval: Qdrant retrieves semantically similar known terms and phrases, allowing the system to generate relevant responses that are contextually aligned.

•	Continuous Learning: While the system currently processes existing vocabulary, it has the potential to address OOV terms by incorporating new data during the ingestion phase, thereby progressively expanding its vocabulary and enhancing adaptability.


---

### 6. **Would you need to self-host? Explain your decision.**

**Answer**:  

Self-hosting data is not necessary for this proof of concept (POC) because I am utilizing Qdrant, which supports regional selection within the U.S., a crucial requirement for managing sensitive internal documentation that must comply with geographical regulations. For this example, I am currently using the free plan, which limits deployment to the EU-East region, while a paid hosting option for the US-West region is available through AWS at a rate of $0.03566 per hour. The code is currently running locally, with the embedding and LLM models accessed via APIs. Additionally, monitoring with MLflow is conducted locally, and there is potential for future cloud implementation

---

### 7. **How did you chunk the documents provided? Does this decision have any effect on the performance of the system?**

**Answer**:  

I utilized Langchain's RecursiveCharacterTextSplitter to segment documents into coherent paragraphs. Through experimentation with chunk size and overlap, I sought the optimal balance between context preservation and processing efficiency. Additionally, I explored the ChunkViz tool to refine my approach to data segmentation, ultimately deciding to leverage sentence embeddings. Results in exp3 show that there is moderate improvement in comparison with exp4 where only the chunk size was changed from 900 to 1500 and the overlap from 150 to 100.

---

### 8. **What is missing for your solution to be production-ready?**

To make the solution production-ready, additional testing is required to identify the optimal combination of embeddings and large language models (LLMs). This includes evaluating accuracy and monitoring processing times to ensure efficiency and reliability in real-world applications. Furthermore, it is crucial to test with larger internal datasets to comprehensively assess overall performance and accuracy. 
Additionally, the solution will be prepared for deployment to the cloud using Docker, and efforts will be made to create a user-friendly application with an enhanced user interface (UI) to improve the overall user experience.
  

---

### 9. **Is your system able to handle changing information? What would happen if the documentation is updated?**

**Answer**:  

Currently, the system cannot handle changing information effectively. When the documentation is updated, the system is unable to generate answers to user questions based on the latest information. However, if the documentation is updated, the vector store can be refreshed by reprocessing the new content and updating the embeddings. By regularly refreshing the data and embeddings, the system can provide users with current and relevant information, allowing it to adapt effectively to any changes in the documentation. A better option would be to employ a mechanism that checks for the existence of documents and updates only the new content.

---

### 10. **How can you evaluate your system?**

**Answer**:  
For evaluation, I utilized the RAGAS framework to calculate three key metrics: Faithfulness, Answer Relevancy, and Context Utilization. I employed an LLM with a higher number of trainable parameters, specifically the Mistral-large-latest model with 128 billion parameters and the Llama3-70B-8192. By using an LLM as a judge, I don’t need user-provided ground-truth to evaluate the system. This is benefitial when there is lack of labeled data especially for problems such as in the assignment.
Faithfulness measures how consistently the generated answer reflects the provided context, with scores scaled from (0,1) where higher values indicate better alignment. An answer is deemed faithful if all its claims can be inferred from the context.
Answer Relevancy assesses the relevance of the generated answer to the prompt. Lower scores indicate incomplete or redundant answers, while higher scores reflect better pertinence. This is calculated as the mean cosine similarity between the original question and artificially generated questions based on the answer.
Lastly, Context Utilization evaluates the effectiveness of the retrieval process. I chose the RAGAS framework for its user-friendly interface and straightforward implementation. 

#### (a) **How do you evaluate your information retrieval system?**

**Answer**:  
I used the context utilization to evaluate the retrieval system. Context utilization is a metric that evaluates whether all of the answer relevant items present in the contexts are ranked higher or not. Ideally all the relevant chunks must appear at the top ranks. This metric is computed using the question, answer and the contexts, with values ranging between 0 and 1, where higher scores indicate better precision.

#### (b) **What would need to be different between evaluation during development and for production?**

**Answer**:  
In production, evaluation would require larger datasets for testing, potentially incorporating ground truth data to establish benchmarks for performance. This ensures that the system is validated against real-world scenarios, providing a more robust assessment of its effectiveness compared to the smaller test sets used during development.


---

