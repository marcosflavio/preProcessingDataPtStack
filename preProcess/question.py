class Question:

    def __init__(self, title, post_id):
        self.title = title
        self.post_id = post_id

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_post_id(self, posttypeid):
        self.post_id = posttypeid

    def get_post_id(self):
        return self.post_id
