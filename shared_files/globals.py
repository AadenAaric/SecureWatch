__Tokens = ""
__listTokens = []


def setDevToken(token):
    global __Tokens
    __Tokens = token

def getDevToken():
    global __Tokens
    return __Tokens

def addinTokens(token):
    global __listTokens
    __listTokens.append(token)


def GetListofToken():
    global __listTokens
    return __listTokens

def deleteToken(token):
    global __listTokens
    if token in __listTokens:
        __listTokens.remove(token)

from threading import Thread
def run():
    while True:
        global __listTokens
        print(__listTokens)
        import time
        time.sleep(5)

