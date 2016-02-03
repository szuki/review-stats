#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import time
import datetime

ACTIVITY_URL = 'http://stackalytics.com/api/1.0/activity?' \
      'user_id=%s&module=fuel-group&page_size=100500&start_record=0'

REVIEW_URL = 'https://review.openstack.org/%s'

def main(args):
    print 'Fetching stats...'
    req = requests.get(ACTIVITY_URL % args.user)
    print 'Done.'
    activities = req.json()['activity']
    unique_reviews = {}
    past = datetime.date.today() - datetime.timedelta(days=5)
    unique = set()
    
    for a in activities:
        if a['gerrit_id'] in unique:
            continue
        unique.add(a['gerrit_id'])
        adate = datetime.date.fromtimestamp(a['date'])
        if adate > past:
            unique_reviews.setdefault(adate, []).append(a['parent_url'])
    for k,v in unique_reviews.iteritems():
        print k
        for e in v:
            print e


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Review story point counter tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='./review-stats.py [-h] GERRIT-USER-ID'
    )
    parser.add_argument('user', type=str,
                        help='Gerrit user id')
    exit(main(parser.parse_args()))
