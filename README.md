# gpt_cv_adapter

It's a Python app that takes your CV and a list of jobs to generate adapted CVs for each job.

## Installation

1. **Clone the repository:**

```sh
git clone https://github.com/navidshad/gpt_cv_adapter.git
cd gpt_cv_adapter
```

2. **Set up a Python virtual environment:**

Make sure you have Python 3.9 or higher installed.

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the python required dependencies:**

```sh
pip install -r requirements.txt
```

4. **Install js dependencies**:

```sh
npm install puppeteer-core
```

## Usage

1. **How to Use**: Watch This video to see how to use the app: [Loom Video](https://www.loom.com/share/0aabaa53c61b44dea2400225eed4e4e0?sid=3dabed6c-d7a2-4a9c-af69-ebf85da6ecac)


2. **Environment Variable**: Create a `.env` file in the root directory of the project and add the following environment variables:

```sh
OPENAI_API_KEY=

FULL_NAME = Your Name

JOBS_DIR = data/jobs
CV_ADAPTED_DIR = data/cv_adapted
CV_FILE_NAME = data/cv.txt

TEMPLATE_FILE_NAME = templates/tailwind_01.html

# These are steps to generate adapted CVs
# Any step can be skipped by setting it to False
# Ensure that you complete the previous steps before proceeding to the next. For example, to generate HTML in step 2, you must first generate the CV in step 1. You can set `ALLOW_NEWCV_AND_COVER = False` only if the CV has already been generated in a previous run.

# Step 1: Generate new CVs with cover letters
ALLOW_NEWCV_AND_COVER = True
# Step 2: Generate an HTML from the step 1
ALLOW_HTML = True
# Step 3: Generate a PDF from the step 2
ALLOW_PDF = True
```

