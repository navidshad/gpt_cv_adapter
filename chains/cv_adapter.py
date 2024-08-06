from langchain.chat_models import ChatOpenAI
from utils.file import read_file_content

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
Perform the following steps:
"""

instructions = read_file_content("prompts/cv.prompt.txt")
human_template += instructions

human_template += """
Note: Return only a JSON object like this {json_object} and nothing else.
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
            model="gpt-4o-mini",
        ),
        prompt=chat_prompt,
    )
