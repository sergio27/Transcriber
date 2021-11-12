
class Error:

    def __init__(self, filename, category, content, text):
        self.filename = filename
        self.category = category
        self.content = content

        if isinstance(text, str):
            self.text = text
        else:
            self.text = text["text"]
