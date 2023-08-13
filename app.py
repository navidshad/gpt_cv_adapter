from utils.file import *
from chains.cv_adapter import get_cv_chain
from chains.template_adapter import get_template_chain


# read value from .env file
def read_env(key):
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith(key):
                return line.split("=")[1].strip()


def run_templlate_adapter_and_save(job_title, md_file: str, html_templates: str = ""):
    html_file_name = f"{cv_adapted_dir}/{job_title}.html"
    md_file_content = read_file_content(md_file)

    result = template_chain.run(
        {
            "md_content": md_file_content,
            "template": html_templates,
        }
    )

    # get job name without extension
    md_file = md_file.split(".")[0]

    write_file_content(html_file_name, result)


# Prepare Chains
openai_api_key = read_env("OPENAI_API_KEY")
cv_chain = get_cv_chain(openai_api_key)
template_chain = get_template_chain(openai_api_key)

# Read CV & Job Description from file
jobs_dir = ".jobs"
cv_adapted_dir = ".cv_adapted"
cv_content = read_file_content("cv.txt")
html_templates = read_file_content("templates/blue_header.html")
jobs = get_files_list(jobs_dir, ".txt")
total_jobs = len(jobs)

print(f"Found {total_jobs} jobs")
counter = 1

for job in jobs:
    # get job name without extension
    job_title = job.split(".")[0]
    md_file_name = f"{cv_adapted_dir}/{job_title}.md"

    print(f"{counter}/{total_jobs} Is running - {job_title}")

    # continue if file is already exist
    if not is_file_exist(md_file_name):
        job_description = read_file_content(f"{jobs_dir}/{job}")
        result = cv_chain.run(
            {
                "cv_content": cv_content,
                "job_description": job_description,
            }
        )

        write_file_content(md_file_name, result)

    print(f"{counter}/{total_jobs} Running Template Adapter for {job_title} CVs")
    run_templlate_adapter_and_save(job_title, md_file_name, html_templates)

    counter += 1

print("Done!")
