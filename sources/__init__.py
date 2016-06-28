from dominate.tags import *
import uuid

class Chapter:
    def __init__(self, title=None, subtitle=None):
        self.name = uuid.uuid4()

        self.chapter = article(_class="chapter")

        self.chapter.add(h1(title, id=self.name))
        if subtitle:
            self.chapter.add(p(subtitle, _class="subtitle"))
        self.chapter.add(hr())

        self.content = self.chapter.add(div(_class="content"))
        self.appendixes = []

    def add(self, what):
        return self.content.add(what)

    def add_appendix(self, appendix):
        appendix.add(br())
        appendix.add(a("<< Back", href="#{0}".format(self.name), _class="backToChapter"))
        return self.appendixes.append(appendix)

class Appendix:
    def __init__(self, title=None, subtitle=None, name=None):
        self.appendix = article(_class="appendix")

        if name:
            self.name = name
        else:
            self.name = str(uuid.uuid4())

        self.appendix.add(h4(title, id=self.name))
        if subtitle:
            self.appendix.add(p(subtitle, _class="subtitle"))

        self.content = self.appendix.add(div(_class="content"))

    def add(self, what):
        return self.content.add(what)
