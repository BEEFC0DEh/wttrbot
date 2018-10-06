import requests
import pprint


def main():
    url = "https://api.telegram.org/bot{}/"
    pp = pprint.PrettyPrinter(indent = 4)
    
    with open('token.txt') as file:
        token = file.readline()
        url = url.format(token)
        
    print(url)
    
    response = requests.get(url + 'getUpdates')
    pp.pprint( response.json() )

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
