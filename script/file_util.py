import os


def get_file(file_name):
    with open(file_name, "rb") as file_stream:
        content = file_stream.read()
        file_stream.close()

    return content


def put_file(file_name, content):
    with open(file_name, "w") as file_stream:
        file_stream.write(content)
        file_stream.close()


def read_chunks(file_stream):
    while True:
        chunk = file_stream.read(4092)
        if not chunk:
            break
        yield chunk


def write_chunk(file_stream, chunk):
    file_stream.write(chunk)


def take_file(key_path):
    result = get_file(key_path)
    os.remove(key_path)
    return result
