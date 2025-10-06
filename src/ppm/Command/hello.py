class Command:
    def __init__(self):
        self.version = '0.1'
        self.author = 'Stevesuk0 <stevesukawa@outlook.com>'
        self.module_desc = 'Say \"Hello, World!\"'

    def on_execute(self, *args):
        print('Hello, World!')