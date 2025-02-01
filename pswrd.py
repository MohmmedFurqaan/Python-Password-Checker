import requests
import sys
import hashlib

#1. request to the API Server
def reuest_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code} check the url and try again')
    return res

def get_password_leak(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def hash_generator(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = reuest_api_data(first5_char)
    # print(response)
    return get_password_leak(response, tail)

def main(args):
    for pswrds in args:
        count = hash_generator(pswrds)
        if count:
            print(f'This Password {pswrds} has been leaked {count} times ..')
        else:
            print('No leak COunts Fetched !')
    return 'Done !'
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
