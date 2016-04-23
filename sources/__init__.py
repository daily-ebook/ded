from dominate.tags import *

class Chapter:
  def __init__(self, title = None, subtitle = None):
    self.chapter = div(_class="chapter")
    cHeader = self.chapter.add(header())
    cHeader.add(h1(title))
    if subtitle:
      cHeader.add(p(subtitle,_class="subtitle"))

    self.content = self.chapter.add(div(_class="content"))
    self.appendixes = []  

  def add(self, what):
    return self.content.add(what)

  def addAppendix(self, appendix):
    return self.appendixes.append(appendix)

class Appendix:
  def __init__(self, title = None, subtitle = None):
    self.appendix = div(_class="appendix")
    aHeader = self.appendix.add(header())
    aHeader.add(h2(title))
    if subtitle:
      aHeader.add(p(subtitle,_class="subtitle"))

    self.content = self.appendix.add(div(_class="content"))

  def add(self, what):
    return self.content.add(what)
