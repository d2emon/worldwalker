class Screen:
    def __init__(self, width=800, height=600, caption=''):
        self.WIDTH = width
        self.HEIGHT = height
        self.SIZE = (self.WIDTH, self.HEIGHT)
        self.CAPTION = caption
        self.CENTER = (self.WIDTH / 2, self.HEIGHT / 2)
