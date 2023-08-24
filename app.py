import json
from utils.file import *
from utils.prompt import *
from chains.cv_adapter import get_cv_chain
from chains.template_adapter import get_template_chain

# allow to generate:
allow_newcv_and_cover = get_env_variable("ALLOW_NEWCV_AND_COVER")
allow_html = get_env_variable("ALLOW_HTML")
allow_pdf = get_env_variable("ALLOW_PDF")

# Prepare Chains
openai_api_key = get_env_variable("OPENAI_API_KEY")
cv_chain = get_cv_chain(openai_api_key)
template_chain = get_template_chain(openai_api_key)

# Read CV & Job Description from file
full_name = get_env_variable("FULL_NAME")
jobs_dir = get_env_variable("JOBS_DIR")
cv_adapted_dir = get_env_variable("CV_ADAPTED_DIR")
cv_content = read_file_content(get_env_variable("CV_FILE_NAME"))
html_templates = read_file_content(get_env_variable("TEMPLATE_FILE_NAME"))
jobs = get_files_list(jobs_dir, ".txt")
total_jobs = len(jobs)

print(f"Found {total_jobs} jobs")
counter = 1

for job in jobs:
    job_title = job.split(".")[0]
    job_dir = os.path.join(cv_adapted_dir, job_title)

    # create job dir if not exist
    if not os.path.exists(job_dir):
        os.makedirs(job_dir)

    md_file_name = f"{job_dir}/{job_title}.md"
    coverletter_file_name = f"{job_dir}/{job_title} _cover.txt"
    html_file_name = f"{job_dir}/{full_name} CV.html"
    pdf_file_name = f"{job_dir}/{full_name} CV.pdf"

    job_description = read_file_content(f"{jobs_dir}/{job}")

    if allow_newcv_and_cover and not is_file_exist(md_file_name):
        print(f"{counter}/{total_jobs} Running CV adapter for {job_title}")
        result = cv_chain.run(
            {
                "cv_content": cv_content,
                "job_description": job_description,
                "json_object": '{"cv": "[new_cv]", "cover_letter": "[cover_letter]"}',
            }
        )

        result = evaluate_promp_result(result)

        # pars the result as json `{ "cv": "{new_cv}", "cover_letter": "{cover_letter}" }`
        result = json.loads(result)
        cv = result["cv"]
        cover_letter = result["cover_letter"]

        write_file_content(md_file_name, cv)
        write_file_content(coverletter_file_name, cover_letter)

    if allow_html and not is_file_exist(html_file_name):
        print(f"{counter}/{total_jobs} Running Template adapter for {job_title}")

        md_file_content = read_file_content(md_file_name)
        result = template_chain.run(
            {
                "md_content": md_file_content,
                "template": html_templates,
            }
        )

        result = evaluate_promp_result(result)

        write_file_content(html_file_name, result)

    if allow_pdf and not is_file_exist(pdf_file_name):
        print(f"{counter}/{total_jobs} Running PDF converter for {job_title}")

        # find script path
        script_path = os.path.dirname(os.path.realpath(__file__))

        # rum nodejs script to convert html to pdf, put full HTML_FILE_PATH as env variable for nodejs script
        os.environ["HTML_FILE_PATH"] = os.path.join(script_path, html_file_name)
        os.system("node pdf_generator.js")

    counter += 1

print("Done!")
