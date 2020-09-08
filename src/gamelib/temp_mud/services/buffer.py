import uuid
from ..errors import ServiceError
from .log import LogService


class BufferOverflowError(ServiceError):
    pass


class ShortBufferOverflowError(BufferOverflowError):
    pass


class BufferService:
    __MAX_LENGTH = 235
    __MAX_BUFFER = 4095

    __buffers = {}

    @classmethod
    def __get_buffer_id(cls, **kwargs):
        buffer_id = kwargs.get('buffer_id')
        if cls.__buffers.get(buffer_id) is None:
            raise ServiceError()

    @classmethod
    def put(cls):
        buffer_id = uuid.uuid1()
        cls.__buffers[buffer_id] = ''
        return {
            'result': True,
            'buffer_id': buffer_id,
        }

    @classmethod
    def post(cls, **kwargs):
        buffer_id = cls.__get_buffer_id(**kwargs)
        text = kwargs.get('text', '')

        if len(text) > cls.__MAX_LENGTH:
            LogService.post_system(message="Bprintf Short Buffer overflow")
            raise ShortBufferOverflowError("Internal Error in BPRINTF")

        text = cls.__buffers.get(buffer_id, '') + text
        if len(text) > cls.__MAX_BUFFER:
            LogService.post_system(message="Buffer overflow on buffer {}".format(buffer_id))
            raise BufferOverflowError("PANIC - Buffer overflow")

        cls.__buffers[buffer_id] = text
        return {
            'result': True,
        }

    @classmethod
    def push_clear(cls, **kwargs):
        buffer_id = cls.__get_buffer_id(**kwargs)
        cls.__buffers[buffer_id] = ''
        return {
            'result': True,
        }

    @classmethod
    def get(cls, **kwargs):
        buffer_id = cls.__get_buffer_id(**kwargs)
        return {
            'result': True,
            'text': cls.__buffers.get(buffer_id, ''),
        }

    @classmethod
    def delete(cls, **kwargs):
        buffer_id = cls.__get_buffer_id(**kwargs)
        del cls.__buffers[buffer_id]
        return {
            'result': True,
        }
