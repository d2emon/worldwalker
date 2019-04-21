class InputBoard:

    @classmethod
    def reprint(cls):
        cls.buffer.need_linebreak = True
        cls.buffer.pbfr()

        if not cls.buffer.pr_due:
            return
        cls.buffer.pr_due = False

        print("\n{}{}".format(cls.prompt, cls.input_buffer))
