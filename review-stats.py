#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import time

ACTIVITY_URL = 'http://stackalytics.com/api/1.0/activity?' \
      'user_id=%s&module=fuel-group&page_size=100500&start_record=0'

REVIEW_URL = 'https://review.openstack.org/%s'

def main(args):
    print 'Fetching stats...'
    req = requests.get(ACTIVITY_URL % args.user)
    print 'Done.'
    activities = req.json()['activity']
    unique_reviews = []
    for a in activities:
        if a['parent_url'] not in unique_reviews:
            unique_reviews.append(a['parent_url'])
    if args.last_review_id:
        last_review_url = REVIEW_URL % args.last_review_id
        if last_review_url not in unique_reviews:
            print 'Invalid review id.'
            exit(1)
        unique_reviews = unique_reviews[:unique_reviews.index(last_review_url)]
    print 'Stats:'
    for u in unique_reviews:
        print u
    print 'Totals: %d' % len(unique_reviews)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Review story point counter tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='./review-stats.py [-h] GERRIT-USER-ID LAST-REVIEW-ID'
    )
    parser.add_argument('user', type=str,
                        help='Gerrit user id')
    parser.add_argument('last_review_id', type=str, nargs='?', default='',
                        help='Last tracked review id. https://review.openstack.org/#/c/[REVIEW-ID]/')
    exit(main(parser.parse_args()))