class Buffer:
    __buffers = dict()
    pr_due = False

    def __init__(self, user_id):
        self.user_id = user_id
        self.text = ""
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

    def dcprnt(self, text=None, output=None):
        text = text or self.text
        # print("\tdcprnt", output, text)
        return text

    def fetch_buffer(self):
        result = ""

        # block_alarm()
        # World.close()
        if self.text:
            self.pr_due = True

        if self.text and self.need_linebreak:
            result += "\n"
        self.need_linebreak = False

        if self.__log_file is not None:
            self.__is_keyboard = False
            self.dcprnt(output=self.__log_file)

        if self.snoopd is not None:
            f = opensnoop(self.snoopd.name, "a")
            if f is not None:
                self.__is_keyboard = False
                self.dcprnt(output=f)
                f.fcloselock()

        self.__is_keyboard = True
        result = self.dcprnt()
        self.text = ""  # clear buffer

        # if self.__snoopt is not None:
        #     viewsnoop()
        # unblock_alarm()
        return result

    def send_raw(self, text):
        self.text += text

    def bprintf(self, text):
        self.text += "%{}%".format(text)
