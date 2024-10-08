# LokaDocAssistant
LokaDocAssistant is a proof of concept (POC) tool designed to help developers efficiently navigate AWS documentation. This tool reduces the time spent searching for information by leveraging natural language processing (NLP) techniques to understand developer queries and retrieve relevant answers from indexed documentation.

## Directory Structure

```bash
LokaDocAssistant
├── configs
│   └──  configuration.yaml
├── data
│   └── sagemaker_documentation
├── src
│   ├── constants
│   │   ├── eval_config.py
│   │   ├── prompt.py
│   │   └── questions.py
│   ├── models
│   │   ├── data_ingester.py
│   │   └── rag.py
│   ├── utils
│   │   ├── evaluation.py
│   │   └── load_configuration.py
│   └── workflows
│       ├── inference_workflows.py
│       └── ingestion_workflows.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── sagemaker_documentation.zip
└── Senior_ML_Tech_Assessment.pdf
```


