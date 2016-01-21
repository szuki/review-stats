#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import time

URL = 'http://stackalytics.com/api/1.0/activity?' \
      'user_id=%s&module=fuel-group&page_size=100500&start_record=0'

def main(args):
    print 'Fetching stats...'
    req = requests.get(URL % args.user)
    print 'Done.'
    activities = req.json()['activity']
    to_time = time.time()
    from_time = time.time() - 7*24*3600
    activities = [a for a in activities if from_time<=a['date']<=to_time]
    unique_reviews = []
    for a in activities:
        if a['parent_url'] not in unique_reviews:
            unique_reviews.append(a['parent_url'])

    print 'Stats:'
    for u in unique_reviews:
        print u
    print 'Totals: %d' % len(unique_reviews)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Review story point counter tool',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='./review-stats.py [-h] [options] GERRIT-USER-ID'
    )
    parser.add_argument('user', type=str,
                        help='Gerrit user id')
    parser.add_argument('-f', '--from', dest='from_date', type=str,
                        default=None, help='Begin of watched period')
    parser.add_argument('-t', '--to', dest='to_date', type=str,
                        default=None, help='Begin of watched period')
    exit(main(parser.parse_args()))