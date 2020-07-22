import string
import random
def generateUniqueID(len):
  characters = string.ascii_letters + string.digits
  return ''.join([random.choice(characters) for _ in range(len)])

def retry(func, max_tries=2):
  tries = 0
  lastError = None
  while tries < max_tries:
    tries += 1
    try: 
      func()
      return
    except Exception as e:
      lastError = e
  raise lastError