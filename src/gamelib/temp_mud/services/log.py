import logging
from datetime import datetime


class LogService:
    __log = []

    @classmethod
    def post_system(cls, **kwargs):
        message = kwargs.get('message')
        message = "{}:  {}\n".format(datetime.now(), message)
        cls.__log.append(message)
        logging.info(message)
        # try:
        #     x = connect(LOG_FILE, "a")
        #     fprintf(x, "{}:  {}\n".format(time(), message))
        #     fclose(x)
        # except FileNotFoundError:
        #     raise LooseError("Log fault : Access Failure")
        return True
