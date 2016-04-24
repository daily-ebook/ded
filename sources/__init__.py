from dominate.tags import *
import uuid

class Chapter:
  def __init__(self, title = None, subtitle = None):
    self.chapter = div(_class="chapter")
    cHeader = self.chapter.add(div(_class="header"))
    cHeader.add(h1(title))
    if subtitle:
      cHeader.add(p(subtitle,_class="subtitle"))
    cHeader.add(hr())

    self.content = self.chapter.add(div(_class="content"))
    self.appendixes = []  

  def add(self, what):
    return self.content.add(what)

  def addAppendix(self, appendix):
    return self.appendixes.append(appendix)

class Appendix:
  def __init__(self, title = None, subtitle = None, name=None):
    self.appendix = div(_class="appendix")
    
    if name:
      self.name = name
    else:
      self.name = str(uuid.uuid4())

    self.appendix.add(a(id=self.name))

    aHeader = self.appendix.add(div(_class="header"))
    aHeader.add(h4(title))
    if subtitle:
      aHeader.add(p(subtitle,_class="subtitle"))

    self.content = self.appendix.add(div(_class="content"))

  def add(self, what):
    return self.content.add(what)
