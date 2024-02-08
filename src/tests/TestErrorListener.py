from antlr4.error.ErrorListener import ErrorListener

class TestErrorListener(ErrorListener):
    def __init__(self):
        super(TestErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append((line, column, msg, offendingSymbol, e))

    def hasErrors(self):
        return len(self.errors) > 0

    def getErrors(self):
        return self.errors
