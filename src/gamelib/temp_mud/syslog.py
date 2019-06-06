from .errors import LooseError


def syslog(message):
    try:
        x = openlock(LOG_FILE, "a")
        fprintf(x, "{}:  {}\n".format(time(), message))
        fclose(x)
    except FileNotFoundError:
        raise LooseError("Log fault : Access Failure")
