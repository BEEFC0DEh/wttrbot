import requests
import pprint

lastUpdateId = 0
url = "https://api.telegram.org/bot{}/"
pp = pprint.PrettyPrinter(indent = 2).pprint

def getUpdates(offset=None, timeout=30):
    params = {'offset': offset, 'timeout': timeout}
    response = requests.get(url + 'getUpdates', params)
    
    if  response.status_code != 200:
        print("ERROR IN GET!")
        return []
    
    json = response.json()
    print(response.text)
    pp(json)
    
    return json['result']

def sendMessage(chatId, message='trololo'):
    params = {'chat_id': chatId, 'text': message, 'parse_mode': 'Markdown'}
    response = requests.get(url + 'sendMessage', params)
    
    if  response.status_code != 200:
        print("ERROR IN SEND!")
        print(response.text)

def sendPhotoUrl(chatId, photoUrl):
    # TODO: check for empty photoUrl
    params = {'chat_id': chatId, 'photo': photoUrl}
    response = requests.get(url + 'sendPhoto', params)
    
    if  response.status_code != 200:
        print("ERROR IN SEND!")
        print(response.text)
        
def sendPhoto(chatId, photo):
    params = {'chat_id': chatId}
    files = {'photo': photo}
    response = requests.post(url + 'sendPhoto', data=params, files=files)
    
    if  response.status_code != 200:
        print("ERROR IN SEND!")
        print(response.text)

#----Command definitions----        
def defaultAction(message, *args):
    chatId = message['chat']['id']
    sendMessage( chatId, 'DOES NOT COMPUTE! @{}'.format(message['chat']['username']) )
    
helpMsg = (
'''/help - this help
/wttr [city] - get wttr''')
    
def sendHelp(message, *args):
    chatId = message['chat']['id']
    sendMessage(chatId, helpMsg)

import re
    
def getWttr(message, *args):
    chatId = message['chat']['id']
    city = args[0]
    if not city:
        city = "Oymyakon"
        
#    photoUrl = 'https://wttr.in/{}_0qp.png'.format(city)
#    rqst = requests.get(photoUrl)
        
#    sendPhoto(chatId, rqst.content)
    
    wttrUrl = 'https://wttr.in/{}'.format(city)
    wttr = requests.get(wttrUrl)
    plainWttr = re.sub(r'\[.*?[\d;].*?m', '', wttr.text)
    lines = plainWttr.split('\n')
    plainWttr = '\n'.join(lines[:6]) + '\n ' # TODO: properly cut the last line
    print(plainWttr)
    sendMessage(chatId, "```" + plainWttr + "```")

supportedCommands = {
     '/help': sendHelp
    ,'/wttr': getWttr
    }
        
def parseCommand(message):
    try:
        command = message['text'].split() # TODO: parse /command@BOTNAME syntax
        try:
            print( 'Got command {}'.format(command) )
            supportedCommands[ command[0] ]( message, command[1:] )
        except KeyError as e:
            print( 'Command {} is unknown'.format(e) )
            defaultAction(message)
    except:
        pp(message)
        print('Wrong message format.')
#----Command definitions----


def main():
    with open('token.txt') as file:
        token = file.readline().rstrip()
        global url
        url = url.format(token)
        
    print(url)
    
    while True:    
        global lastUpdateId
        result = getUpdates(lastUpdateId)
        if len(result) > 0:
            lastUpdateId = result[-1]['update_id']
            print(lastUpdateId)
            lastUpdateId += 1
            
            knownChats = {}
            for update in result:
                try:
                    message = update['message']
                    chatId = message['chat']['id']
                    updateId = update['update_id']
                    
                    if chatId in knownChats:
                        if updateId > knownChats[chatId]['update_id']:
                            knownChats[chatId] = update
                    else:
                        knownChats[chatId] = update
                        print(chatId)
                except:
                    pp(update)
                    print('Wrong update format.')
            
            for chatId, update in knownChats.items():
                parseCommand( update['message'] )

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
