from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain

template = """
You are a helpful assistant who can convert an markdown CV content into html temlate.
- This is a markdown CV content in tech industry:
`{md_content}`
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
system_message_prompt.input_variables.append("md_content")

human_template = """
- This is the html template, attention to comments I put in the html template.
`{template}`

Generate a ready to use html content and return the html content only nothing more. return the html content without any wrapper or comments.
"""

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
human_message_prompt.input_variables.append("template")

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)


def get_template_chain(openai_api_key):
    return LLMChain(
        llm=ChatOpenAI(
            openai_api_key=openai_api_key,
            model="gpt-3.5-turbo-16k",
        ),
        prompt=chat_prompt,
    )
