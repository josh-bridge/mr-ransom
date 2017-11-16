import os


def put_file(content, file_name):
    with open(file_name, "w") as file_stream:
        file_stream.write(content)
        file_stream.close()


def get_file(file_name):
    with open(file_name, "rb") as file_stream:
        content = file_stream.read()
        file_stream.close()

    return content


def get_current_location():
    return os.path.dirname(os.path.realpath(__file__))


def get_full_path(path):
    return os.path.join(get_current_location(), path)
