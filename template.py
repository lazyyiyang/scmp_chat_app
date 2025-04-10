answer_prompt = """## Role
You are a helpful assistant that provides answers to questions.

## Task
You will be given a question and several reference from different news articles. Your task is to provide a concise answer to the question based on the information in the paragraphs.

## Note
- You should cite the paragraphs you used to answer the question.
- The answer should be short and to the point.

## Question
{question}

## Reference
{reference}

## Answer
"""

ner_prompt = """## Role
You are a helpful assistant that extract key words from the text.

## Task
You will be given a text and your task is to extract the key words from the text.

## Note
- You should extract the key words from the text.
- The key words should be short and to the point.
- key words should be in a list format.

## Question
{question}

## Key words
"""