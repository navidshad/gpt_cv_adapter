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

Perform the following steps:
1. Change the summary of the CV and match it with the job description.
2. Find a proper [Position Title] for the CV based on the job description.
3. Then replace the new summary to the CV content and create a new CV in markdown format.
4. Remove each [Other skills] item of CV cntent if not mentione in the job description.
5. Generate a cover letter for the job description based on the CV content with maximom 2 paragraphs. if ther is skills in the job description that are not in the CV, list them to into cover letter and say I will learn them.
6. then return only a JSON object like this {json_object} and nothing else.
7. you have to return only a JSON object like this {json_object} and nothing else.
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
