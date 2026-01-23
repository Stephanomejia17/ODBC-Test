from io import StringIO


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = StringIO()

    def write(self, text):
        self.text_widget.insert('end', text)
        self.text_widget.see('end')
        self.text_widget.update_idletasks()

    def flush(self):
        pass