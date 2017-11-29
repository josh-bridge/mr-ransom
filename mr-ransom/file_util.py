def get_file(file_path):
    with open(file_path, "rb") as file_stream:
        content = file_stream.read()
        file_stream.close()

    return content


def put_file(file_path, content):
    with open(file_path, "w") as file_stream:
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
