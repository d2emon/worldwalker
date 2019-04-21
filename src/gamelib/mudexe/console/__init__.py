from gamelib.services.buffer import Buffer


class Console:
    def __init__(self, user_id):
        self.prompt = ""
        self.input_buffer = ""
        self.output_buffer = Buffer(user_id)

    def send_raw(self, text):
        self.output_buffer.send_raw(text)

    def show_output(self):
        print(self.output_buffer.fetch_buffer(), end='')

    def get_input(self, prompt, max_length):
        self.output_buffer.bprintf(prompt)
        self.show_output()
        self.output_buffer.pr_due = False

        self.prompt = prompt
        self.input_buffer = input()[:max_length]

        return self.input_buffer
