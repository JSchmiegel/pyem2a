#!/bin/python

import sys
import os
import urllib.request
import emoji
import re

colorFlag = False
args = []
emojiStrs = []

# check if there is no argument or information wanted
def checkArguments(args):
  global colorFlag
  if args == [] or args[0] == '-h' or args[0] == '--help' :
    print('''Usage: em2a <string> [<string> ...]\n\nEach string can contain zero or more raw UTF-8 emojis or :alias:-styled emoji escape sequences.\nOptional the argument --color can be used to get colored emojis''')
    sys.exit()
  if '--color' in args:
    colorFlag = True
    args.remove('--color')

def getUnicode(arg):
  try:
    pattern = re.compile('^:.*:$')
    if pattern.match(arg):
      emojiStr = emoji.emojize(arg, language="alias")
    else:
      emojiStr = arg
    emojiStrs.append(emojiStr)
    return ('{:X}'.format(ord(emojiStr))).lower()
  except:
    print('Error: {arg} is not recognized as an emoji.')


# Extract emojis into images/ if we haven't already done so
def extractEmojis(unicode):
  # TODO: enable also :+1:
  # unicode = '1f44d'
  
  # test if file already exists
  path = f'./images/{unicode}.png'
  file_exists = os.path.exists(path)
  if not file_exists:
    # download emoji
    url = f'https://emoji.aranja.com/static/emoji-data/img-apple-160/{unicode}.png'
    urllib.request.urlretrieve(url, path)


def createImageFolder():
  if not os.path.exists("./images"):
    os.makedirs("images")

def emojis2Ascii(emoji):
  if colorFlag:
    command = f'jp2a --background=light --colors --size=80x30 ./images/{emoji}.png'
  else:
    command = f'jp2a --background=light --size=80x30 ./images/{emoji}.png'
  result = os.popen(command)
  asciiEmoji = result.read()
  return asciiEmoji

if __name__ == "__main__":
  args = sys.argv[1:]
  checkArguments(args)
  createImageFolder()

  asciiEmojis = []
  for arg in args:
    unicode = getUnicode(arg)
    extractEmojis(unicode)
    asciiEmojis.append(emojis2Ascii(unicode))

  for i in range(len(args)):
    print('\n\n')
    print(emojiStrs[i])
    print('\n\n')
    print(asciiEmojis[i])
    print('\n\n')