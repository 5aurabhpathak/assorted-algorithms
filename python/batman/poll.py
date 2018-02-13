import requests, time, ssl

host = 'https://api.coinsecure.in/v1'

def to_url(path): return '{}/{}'.format(host, path)
def make_csvline(response): return ','.join(list(map(str, response.values())))

if __name__ == '__main__':
    with open('data/ticker.csv', 'a', encoding='utf-8', buffering=1) as dbfile:
        prevTimestamp = None
        while True:
            try:
                response = requests.get(to_url('exchange/ticker')).json()['message']
                print(response)
                if response['timestamp'] != prevTimestamp:
                    line = make_csvline(response)
                    print(line)
                    #dbfile.write(line)
                    prevTimestamp = response['timestamp']
            except ssl.SSLEOFError: print('Non-fatal error occured.')
            time.sleep(1)