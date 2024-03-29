import base64


def get_file(file_path):
    with open(file_path, "rb") as file_stream:
        content = file_stream.read()
        file_stream.close()

    return content


def get_file_e64(file_path):
    content = []
    for chunk in read_chunks(open(file_path, "rb")):
        content.append(base64.b64encode(chunk))

    return ''.join(content)


def read_chunks(file_stream):
    while True:
        chunk = file_stream.read(4092)
        if not chunk:
            break
        yield chunk


def put_file(file_path, content):
    with open(file_path, "w") as file_stream:
        file_stream.write(content)
        file_stream.close()


def put_file_d64(file_path, content):
    with open(file_path, "w") as file_stream:
        file_stream.write(base64.b64decode(content))
        file_stream.close()
