import os


def get_files_list(path, extension=None):
    files = os.listdir(path)
    if extension is not None:
        files = [f for f in files if f.endswith(extension)]
    return files


def read_file_content(path):
    with open(path, "r") as f:
        return f.read()


def write_file_content(path, content):
    with open(path, "w") as f:
        f.write(content)


def is_file_exist(path):
    return os.path.isfile(path)


def get_env_variable(name):
    with open(".env", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(name):
                try:
                    value = line.split("=")[1].strip()

                    # cast boolean
                    if value.lower() == "true":
                        return True
                    elif value.lower() == "false":
                        return False
                    
                    return value
                except IndexError:
                    return None
