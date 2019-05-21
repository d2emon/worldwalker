from .file_service import TextFileService


class BanFile(TextFileService):
    filename = "ban_file"
    connections = dict()
    content = None
