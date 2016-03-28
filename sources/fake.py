# fake source
import random, string

metadata = {
  "name": "fake",
  "fullname": "Fake Source",
  "description": "This source will provide fake data, as a test.",
  "options": [
    {
      "name": "fakeText",
      "type": "text",
      "required": True
    },
    {
      "name": "fakeNumber",
      "type": "number",
      "default": 0
    }
  ]
}

def build(config):
  source = {}
  source["title"] = "This is fake source"
  source["subtitle"] = "All hail **fake** *source*"
  source["body"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ac varius est. Maecenas id mauris massa. Cras tincidunt, lorem non egestas facilisis, nisl enim ullamcorper nunc, sed laoreet elit turpis viverra mi. Suspendisse potenti. Donec tempus tincidunt metus. Suspendisse a nibh ac nisi consectetur feugiat. Suspendisse nunc est, tempor vel feugiat non, finibus nec arcu. Donec sed augue ultricies, sagittis diam quis, fermentum enim. Suspendisse blandit lectus mauris, eget tempor ipsum varius in. Mauris id rutrum mi. Aliquam malesuada fringilla enim et eleifend. Curabitur rhoncus ligula sit amet turpis ullamcorper, eu consequat sem posuere. Mauris vehicula orci ac faucibus ornare. Sed consequat nisl in porttitor dictum. Etiam eget interdum nulla, id blandit massa. Donec blandit nibh sed feugiat cursus."

  source["chapters"] = []

  for i in range(0,5):
    chap = {}
    chap["title"] = "Title!"
    chap["body"] = ""
    for i in range(0,random.randint(4,12)):
      chap["body"] += randomword(random.randint(1,8)) + " " 
    
    chap["chapters"] = []
    for i in range(0,3):
      subchap = {}
      subchap["title"] = "Title of subchapter"
      subchap["body"] = ""
      for i in range(0,random.randint(4,12)):
        subchap["body"] += randomword(random.randint(1,8)) + " " 
      chap["chapters"].append(subchap)

    source["chapters"].append(chap)

  return source

def randomword(length):
  return ''.join(random.choice(string.ascii_lowercase) for i in range(length))