from question import Question


class PreProcessing:

    def __init__(self, posts, textCleaner):
        self.posts = posts
        self.questions = None
        self.textCleaner = textCleaner

    def create_questions(self):
        for p in self.posts:
            q = Question(p[1], p[0])
            self.questions.append(q)
        self.posts = None
        return self.questions

    # removeRepChar
    def remove_rep_char(self):
        for q in self.questions:
            q.set_title(self.textCleaner.removeRepChar(q.get_title()))
        return self.questions

    # removeSymbols
    def remove_symbols(self):
        for q in self.questions:
            q.set_title(self.textCleaner.removeSymbols(q.get_title()))
        return self.questions

    # removeSufPort
    def remove_sufix_portugues(self):
        for q in self.questions:
            q.set_title(self.textCleaner.removeSufPort(q.get_title()))
        return self.questions

    # removeAccent
    def remove_accent(self):
        for q in self.questions:
            q.set_title(self.textCleaner.removeAccent(q.get_title()))
        return self.questions

    # removeLinks
    def remove_links(self):
        for q in self.questions:
            q.set_title(self.textCleaner.removeLinks(q.get_title()))
        return self.questions

    # removeStopwords
    def remove_stop_words(self):
        for q in self.questions:
            q.set_title(self.textCleaner.removeStopwords(q.get_title()))
        return self.questions

    def get_questions(self):
        return self.questions

    def set_questions(self, questions):
        self.questions = questions
