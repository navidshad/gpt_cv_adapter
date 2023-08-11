from utils.file import *
from chains.cv_adapter import get_cv_chain
from chains.template_adapter import get_template_chain


# read value from .env file
def read_env(key):
    with open(".env", "r") as f:
        for line in f.readlines():
            if line.startswith(key):
                return line.split("=")[1].strip()


jobs_dir = ".jobs"
cv_adapted_dir = ".cv_adapted"

# Prepare Chains
openai_api_key = read_env("OPENAI_API_KEY")
cv_chain = get_cv_chain(openai_api_key)
template_chain = get_template_chain(openai_api_key)

# Read CV & Job Description from file
cv_content = read_file_content("cv.txt")
jobs = get_files_list(jobs_dir, ".txt")
total_jobs = len(jobs)

# Run CV Adapter
print(f"Running CV Adapter for {total_jobs} jobs")
counter = 1
for job in jobs:
    # get job name without extension
    job_title = job.split(".")[0]
    md_file_name = f"{cv_adapted_dir}/{job_title}.md"

    print(f"{counter}/{total_jobs} is running - {job_title}")

    # continue if file is already exist
    if is_file_exist(md_file_name):
        counter += 1
        continue

    job_description = read_file_content(f"{jobs_dir}/{job}")

    result = cv_chain.run(
        {
            "cv_content": cv_content,
            "job_description": job_description,
        }
    )

    write_file_content(md_file_name, result)
    counter += 1

# Run Template Adapter
counter = 1
md_cvs = get_files_list(cv_adapted_dir, ".md")
total_md_cvs = len(md_cvs)
html_templates = read_file_content("templates/blue_header.html")

print(f"Running Template Adapter for {total_md_cvs} CVs")
for md_cv in md_cvs:
    job_title = md_cv.split(".")[0]
    html_file_name = f"{cv_adapted_dir}/{job_title}.html"
    md_cv_content = read_file_content(f"{cv_adapted_dir}/{md_cv}")

    print(f"{counter}/{total_md_cvs} template is running - {job_title}")

    result = template_chain.run(
        {
            "md_content": md_cv_content,
            "template": html_templates,
        }
    )

    # get job name without extension
    md_cv = md_cv.split(".")[0]

    write_file_content(html_file_name, result)

print("Done!")
