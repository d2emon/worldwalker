import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s:%(levelname)s:%(pathname)s:%(lineno)s\n\t%(message)s'
)


class LogService:
    __log = []

    @classmethod
    def post_system(cls, **kwargs):
        message = kwargs.get('message')
        logging.info(message)
        # try:
        #     cls.__log.append(message)
        #     x = connect(LOG_FILE, "a")
        #     fprintf(x, "{}:  {}\n".format(time(), message))
        #     fclose(x)
        # except FileNotFoundError:
        #     raise LooseError("Log fault : Access Failure")
        return True
