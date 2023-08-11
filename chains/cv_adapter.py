from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chains import LLMChain
	
template = """
You are a helpful assistant who generates adapted CV based on a job description.
This is a CV content in tech industry:
`{cv_content}`
"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template);
system_message_prompt.input_variables.append("cv_content")

human_template = """
# This is a job description:
`{job_description}`

Generate a ready to send adapted CV in markdown format.
"""

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
human_message_prompt.input_variables.append("job_description")

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

def get_cv_chain(openai_api_key):
	return LLMChain(
		llm=ChatOpenAI(
			openai_api_key=openai_api_key,
			model="gpt-3.5-turbo-16k",
		),
		prompt=chat_prompt,
	)

