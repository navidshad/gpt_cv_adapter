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
Change the summary of the CV to match the job description, 
Then replace the new summary to the CV content and create a new CV in markdown format and return the new CV only without any extra description, for example dont menttion this is a new CV or etc.
"""

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
human_message_prompt.input_variables.append("job_description")

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
