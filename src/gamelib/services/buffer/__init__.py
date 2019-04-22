from .exceptions import ShortBufferOverflowError, BufferOverflowError


class Decoder:
    def __init__(self, text, output):
        self.__ct = 0
        self.text = text
        self.output = output

    @property
    def character(self):
        return self.text[self.__ct]

    def __to_continue(self, max_length):
        unprocessed = self.text[self.__ct + 1:]
        special_close = unprocessed.find('\001')

        if special_close < 0 or special_close > max_length:
            syslog("IO_TOcontinue overrun")
            self.text = ""
            crapup("Buffer OverRun in IO_TOcontinue")

        self.__ct = special_close + 1
        return unprocessed[:special_close]

    def __decode_special(self, user):
        if self.character == 'f':
            self.__pfile(user)
        elif self.character == 'd':
            return self.__pndeaf(user)
        elif self.character == 's':
            return self.__pcansee(user)
        elif self.character == 'p':
            return self.__prname(user)
        elif self.character == 'c':
            return self.__pndark(user)
        elif self.character == 'P':
            return self.__ppndeaf(text, ct, file)
        elif self.character == 'D':
            return self.__ppnblind(text, ct, file)
        elif self.character == 'l':
            return self.__pnotkb(text, ct, file)
        # self.text = ""
        # loseme()
        raise CrapupError("Internal $ control sequence error\n")

    def __pfile(self, user):
        special_data = self.__to_continue(128)
        if user.debug_mode:
            yield "[FILE {} ]\n".format(special_data)
        f_listfl(self.output)

    def __pndeaf(self, user):
        special_data = self.__to_continue(256)
        if not user.ail_deaf:
            yield special_data

    def __pcansee(self, user):
        username = self.__to_continue(23)
        special_data = self.__to_continue(256)
        a = fpbns(username)
        if not user.seeplayer(a):
            return
        yield special_data

    def __prname(self, user):
        username = self.__to_continue(23)
        if not user.seeplayer(fpbns(username)):
            username = "Someone"
        yield username

    def __pndark(self, user):
        special_data = self.__to_continue(256)
        if not is_dark() and not user.ail_blind:
            yield special_data

    def __ppndeaf(self, user):
        special_data = self.__to_continue(256)
        if not user.ail_deaf:
            yield self.text
        """
        """

    def __ppnblind(self, user):
        special_data = self.__to_continue(256)
        if not user.ail_deaf:
            yield self.text
        """
        """

    def __pnotkb(self, user):
        special_data = self.__to_continue(256)
        if not user.ail_deaf:
            yield self.text
        """
        """

    def decode(self, user):
        while self.__ct < len(self.text):
            if self.character != '\001':
                self.output.putc(self.character)
                self.__ct += 1
            else:
                self.__ct += 1
                self.output.fprintf(self.__decode_special(user))


class Buffer:
    __buffers = dict()
    pr_due = False

    def __init__(self, user_id):
        self.user_id = user_id
        self.__text = ""
        # 4K of chars should be enough for worst case

        self.need_linebreak = False  # pr_qcr
        self.__log_file = None  # log_fl
        self.__is_keyboard = True  # iskb
        self.snoopd = None
        self.__snoopt = None

        self.__buffers[self.user_id] = self

    @classmethod
    def get_buffer(cls, user_id):
        return cls.__buffers[user_id]

    def fetch_buffer(self):
        result = ""

        # block_alarm()
        # World.close()
        if self.__text:
            self.pr_due = True

        if self.__text and self.need_linebreak:
            result += "\n"
        self.need_linebreak = False

        if self.__log_file is not None:
            self.__is_keyboard = False
            self.__dcprnt(output=self.__log_file)

        if self.snoopd is not None:
            f = opensnoop(self.snoopd.name, "a")
            if f is not None:
                self.__is_keyboard = False
                self.__dcprnt(output=f)
                f.fcloselock()

        self.__is_keyboard = True
        result = self.__dcprnt()
        self.__text = ""  # clear buffer

        # if self.__snoopt is not None:
        #     viewsnoop()
        # unblock_alarm()
        return result

    def add_text(self, text):
        self.__text += text

    def bprintf(self, text):
        # Max 240 chars/msg
        if len(text) > 235:
            raise ShortBufferOverflowError()

        # Now we have a string of chars expanded
        self.__quprnt(text)

    def __quprnt(self, text):
        if len(self.__text) + len(text) > 4095:
            raise BufferOverflowError()
        self.add_text(text)

    def __dcprnt(self, text=None, output=None):
        decoder = Decoder(text or self.__text, output)
        return decoder.decode()
