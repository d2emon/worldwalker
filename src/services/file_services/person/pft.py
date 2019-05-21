from services.file_services.file_service import TextFileService


class Pft(TextFileService):
    filename = "pft"
    connections = dict()
    content = []
