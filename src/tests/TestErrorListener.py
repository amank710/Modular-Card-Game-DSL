from antlr4.Token import CommonToken
from antlr4.error.ErrorListener import ErrorListener


class TestErrorListener(ErrorListener):
    INSTANCE = None

    def __init__(self):
        super(TestErrorListener, self).__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if isinstance(offendingSymbol, CommonToken):
            offendingText = offendingSymbol.text
        else:
            offendingText = str(offendingSymbol)

        expectedTokens = recognizer.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)

        error = f"line {line}:{column} mismatched input '{offendingText}' expecting {expectedTokens}"
        self.errors.append(error)

    def hasErrors(self):
        return len(self.errors) > 0

    def getErrors(self):
        return self.errors


TestErrorListener.INSTANCE = TestErrorListener
