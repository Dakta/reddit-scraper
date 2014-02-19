from __future__ import division # we always want floating point

import re
import time
from datetime import datetime, timedelta
from os import path
from spiderbase import SpiderBase, Delay



class Monitor(SpiderBase):

    def __init__(self, username=None, password=None, delay=4, log='comment-scraper.log'):
        #init
        self.spider = SpiderBase(username=username, password=password, delay=delay, log=log)
    
    
    def monitor_comments(self):
        url = 'http://www.reddit.com/comments.json?limit=100'
        newest = None
        comments_per_minute = []
        
        start = datetime.now()
        # while True:
        for i in xrange(0, 30):
            print "Loop #" + str(i)
            
            new_comments, after, next_newest = self._scan_comments(url, newest)
            newest = next_newest
            
            if i != 0:
                elapsed = datetime.now() - start
                print str(elapsed)
                comments_per_minute.append(float(new_comments) / (elapsed.seconds/60))
                
            start = datetime.now()

        print "comments_per_minute = " + str(comments_per_minute)
        print "\navg comments_per_minute = " + str(reduce(lambda x, y: x + y, comments_per_minute) / float(len(comments_per_minute)))

    def _scan_comments(self, url, newest):
        new_comments = 0
        
        data = self.spider._get_json(url)
        
        comments = data['data']['children']
        after = data['data']['after']
        
        for i, c in enumerate(comments):
            comment = c['data']

            if i == 0:
                next_newest = comment['id']
            if comment['id'] <= newest: # comments ids are generated sequentially, so we can compare them like this
                print " comment['id'] == newest"
                break
                
            print " " + comment['id']
            new_comments = new_comments + 1
#             body = comment['body'].lower()
#             for k in self._mentioned_keywords(body):
#                 mention = Mention()
#                 mention.keyword_uid = k.uid
#                 mention.thread_id = comment['link_id'][3:]
#                 mention.comment_id = comment['id']
#                 mention.author = comment['author']
#                 mention.subreddit = comment['subreddit']
#                 mention.created = unix_string(int(comment['created_utc']))
#         session.commit()
        print "new_comments " + str(new_comments) + ", after " + str(after) + ", next_newest " + str(next_newest)
        return (new_comments, after, next_newest)

def main():
    comments = Monitor('***REMOVED***', '***REMOVED***')


if __name__ == "__main__":
    print "Logging in..."
    comments = Monitor('***REMOVED***', '***REMOVED***')
    print "  Success!"
    
    comments.monitor_comments()