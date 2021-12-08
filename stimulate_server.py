#!/usr/bin/env python

import subprocess
import argparse
import time
import random

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Stimulate an HTTPS server vulnerable to Heartbleed')
    parser.add_argument('-t', action = 'store', default = 1, type = int,
        help = 'Time between requests (in seconds). Default is 1 second.')
    parser.add_argument('-a', action = 'store', default = '127.0.0.1',
        type = str,
        help = 'Address of server to be fed with data. Default is 127.0.0.1.')
    args = parser.parse_args()
    print(args.a)

    USER_LIST = [
        'Arrhythmia',
        'Cardiovascular disease',
        'Coronary heart disease',
        'Heart attack',
        'Heart failure',
        'High blood pressure',
        'Stroke',
        'Sudden cardiac arrest',
        'Aorta',
        'Blood clot',
        'Bradycardia',
        'Cholesterol',
        'Collateral vessels',
        'Defibrillator',
        'Open heart surgery',
        'Palpitation',
        'Stress'
    ]

    PASSWORD_LIST = [
        '123456',
        'password',
        'iloveyou',
        'princess',
        'rockyou',
        'abc123',
        'nicole',
        'daniel',
        'babygirl',
        'monkey',
        'lovely',
        'jessica',
        'michael',
        'qwerty',
        'qazwsx',
        'lucky1',
        'potter'
    ]

    while True:
        user = random.choice(USER_LIST)
        password = random.choice(PASSWORD_LIST)
        print('Calling server. User:%s, password:%s' % (user, password))
        subprocess.call([
            'curl',
            '--insecure',
            '-d',
            'user=%s&password=%s' % (user, password),
            '-A',
            'User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0;)',
            '-w',
            '%{http_code} %{url_effective} %{size_request}\n',
            'https://%s' % args.a,
            '-o',
            '/dev/null',
        ])
        time.sleep(args.t)
