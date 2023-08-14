from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain

template = """
You are a CV assistant, and this is the CV content:
```plaintext
{cv_content}
```
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
system_message_prompt.input_variables.append("cv_content")

human_template = """
This is the job description:
```plaintext
{job_description}
```

So perform the following steps:
1. Change the summary of the CV to match the job description,
2. Then replace the new summary to the CV content and create a new CV in markdown format.
3. Generate a cover letter for the job description based on the CV content with maximom 2 paragraphs.
4. then return only a JSON object like this {json_object} and nothing else.
5. you have to return only a JSON object like this {json_object} and nothing else.
"""

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
human_message_prompt.input_variables.append("job_description")
human_message_prompt.input_variables.append("json_object")

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)


def get_cv_chain(openai_api_key):
    return LLMChain(
        llm=ChatOpenAI(
            openai_api_key=openai_api_key,
            model="gpt-3.5-turbo-16k",
        ),
        prompt=chat_prompt,
    )
