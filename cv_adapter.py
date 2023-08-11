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

Generate a CV content that is adapted to the job description in 
 format.
"""

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
human_message_prompt.input_variables.append("job_description")

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(
	llm=ChatOpenAI(
		openai_api_key="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",
		model="gpt-3.5-turbo-16k",
	),
	prompt=chat_prompt,
)

def read_file_content(path):
	with open(path, "r") as f:
		return f.read()
	
def write_file_content(path, content):
	with open(path, "w") as f:
		f.write(content)

# Read CV & Job Description from file
cv_content = read_file_content("cv.txt")
job_description = read_file_content("job.txt")

result = chain.run({
    "cv_content": cv_content,
    "job_description": job_description,
})

write_file_content("cv_adapted.md", result)
