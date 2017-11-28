def get_file(file_name):
    with open(file_name, "rb") as file_stream:
        content = file_stream.read()
        file_stream.close()

    return content


def read_chunks(file_stream):
    while True:
        chunk = file_stream.read(4092)
        if not chunk:
            break
        yield chunk


def write_chunk(file_stream, chunk):
    file_stream.write(chunk)
