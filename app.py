from utils.file import *
from chains.cv_adapter import get_cv_chain
from chains.template_adapter import get_template_chain
from chains.cover_letter_adapter import get_cover_letter_chain


# read value from .env file
def read_env(key):
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith(key):
                return line.split("=")[1].strip()


# Prepare Chains
openai_api_key = read_env("OPENAI_API_KEY")
cv_chain = get_cv_chain(openai_api_key)
template_chain = get_template_chain(openai_api_key)
cover_letter_chain = get_cover_letter_chain(openai_api_key)

# Read CV & Job Description from file
jobs_dir = "data/jobs"
cv_adapted_dir = "data/cv_adapted"
cv_content = read_file_content("data/cv.txt")
html_templates = read_file_content("templates/tailwind_01.html")
jobs = get_files_list(jobs_dir, ".txt")
total_jobs = len(jobs)

print(f"Found {total_jobs} jobs")
counter = 1

for job in jobs:
    job_title = job.split(".")[0]
    md_file_name = f"{cv_adapted_dir}/{job_title}.md"
    html_file_name = f"{cv_adapted_dir}/{job_title}.html"
    pdf_file_name = f"{cv_adapted_dir}/{job_title}.pdf"
    coverletter_file_name = f"{cv_adapted_dir}/{job_title} _cover.txt"
    job_description = read_file_content(f"{jobs_dir}/{job}")

    if not is_file_exist(md_file_name):
        print(f"{counter}/{total_jobs} Running CV adapter for {job_title}")
        result = cv_chain.run(
            {
                "cv_content": cv_content,
                "job_description": job_description,
            }
        )

        write_file_content(md_file_name, result)

    if not is_file_exist(html_file_name):
        print(f"{counter}/{total_jobs} Running Template adapter for {job_title}")

        md_file_content = read_file_content(md_file_name)
        result = template_chain.run(
            {
                "md_content": md_file_content,
                "template": html_templates,
            }
        )
        write_file_content(html_file_name, result)

    if not is_file_exist(coverletter_file_name):
        print(f"{counter}/{total_jobs} Running Cover-Letter adapter for {job_title}")

        result = cover_letter_chain.run(
            {
                "cv_content": cv_content,
                "job_description": job_description,
            }
        )
        write_file_content(coverletter_file_name, result)

    if not is_file_exist(pdf_file_name):
        print(f"{counter}/{total_jobs} Running PDF converter for {job_title}")

        # find script path
        script_path = os.path.dirname(os.path.realpath(__file__))

        # rum nodejs script to convert html to pdf, put full HTML_FILE_PATH as env variable for nodejs script
        os.environ["HTML_FILE_PATH"] = os.path.join(script_path, html_file_name)
        os.system("node pdf_generator.js")

    counter += 1

print("Done!")
