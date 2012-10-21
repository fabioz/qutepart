"""QSyntaxHighlighter implementation
Uses Syntax module for doing the job
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextBlockUserData

from ColorTheme import ColorTheme

class _TextBlockUserData(QTextBlockUserData):
    def __init__(self, data):
        QTextBlockUserData.__init__(self)
        self.data = data


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, syntax, *args):
        QSyntaxHighlighter.__init__(self, *args)
        self._theme = ColorTheme()
        self._syntax = syntax
    
    def highlightBlock(self, text):
        lineData, matchedContexts = self._syntax.parseBlock(text, self._prevData())
        self._syntax.parseAndPrintBlockTextualResults(text, self._prevData())
        contextAreaStartPos = 0
        for context, contextLength, matchedRules in matchedContexts:
            self.setFormat(contextAreaStartPos, contextLength, self._theme.getFormat(context.attribute))
            for rule, pos, ruleLength in matchedRules:
                if rule.attribute is not None:
                    self.setFormat(pos, ruleLength, self._theme.getFormat(rule.attribute))
            contextAreaStartPos += contextLength
        
        self.setCurrentBlockUserData(_TextBlockUserData(lineData))

    def _prevData(self):
        prevBlock = self.currentBlock().previous()
        if prevBlock.isValid():
            dataObject = prevBlock.userData()
            if dataObject is not None:
                return dataObject.data
        return None
