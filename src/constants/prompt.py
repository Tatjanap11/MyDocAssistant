"""Prompt constants for the LLM generator"""

LLAMA_3_PROMPT = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|> {system_message} <|eot_id|>
<|start_header_id|>user<|end_header_id|> {user_message}

-----------
This is the context:
{{context}}

-----------
This is the question:
{{question}}
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
"""

SYSTEM_MESSAGE = """
You are an AI assistant that helps users with answering queries about documentation. You have access to a large collection of documents 
from AWS documentation, particularly SageMaker and have to answer in details and explain clearly.
"""

USER_MESSAGE = """
Please answer my question about AWS documentation only based on provided context.
"""
