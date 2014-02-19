from __future__ import division # we always want floating point

import re
import time
import logging

from datetime import datetime, timedelta
from multiprocessing import Process, current_process


from spiderbase import SpiderBase

from models import cfg_file, path_to_cfg, session
from models import Comment


class Monitor(SpiderBase):

    def __init__(self, username=None, password=None, delay=4, logfile='comment-scraper.log'):
        #logging
        self.logger = logging.getLogger('comment-scraper')
        self.logger.addHandler(logging.FileHandler(logfile))
        self.logger.addHandler(logging.StreamHandler()) # print to std out for debugging
        self.logger.setLevel(logging.DEBUG)

        #init
        self.delay = delay
        self.limit = 100 # TODO: Add automatic limit adjustment to minimize network load
        self.spider = SpiderBase(username=username, password=password)
    
    def monitor_comments(self):
        url = 'http://www.reddit.com/comments.json?limit=25'
        newest_id = None

        # get the ID the first time, but don't process
        data, next_newest_id, after = self._parse_json(url)

        while True:
            start = datetime.now()
                        
            data, newest_id, after = self._parse_json(url)
            
            # we don't want to process the first page, else we risk infinite recursion
            self.logger.debug("Starting new Comment Parser")
            p = Process(name='Comment Parser', target=self._process_comments, args=(url, next_newest_id, data, after))
            p.start()
            
            # increment
            next_newest_id = newest_id
            
            sleep = start + timedelta(seconds=self.delay) - datetime.now()
            self.logger.debug("Sleeping for %s" % sleep)
            
            # from http://stackoverflow.com/questions/2880713/time-difference-in-seconds-as-a-floating-point#comment2931070_2880735
            sleep = sleep.seconds + (float(1) / sleep.microseconds)
            
            time.sleep( sleep )

    def _parse_json(self, url, after=None):
        if after is not None:
            url = "%s&after=%s" % (url, after)
        
        data = self.spider._get_json(url)
        newest_id = data['data']['children'][0]['data']['id']
        after = data['data']['after']
        
        return (data, newest_id, after)


    def _process_comments(self, url, next_newest_id, data, after):
        """Threaded comment parser"""
        
        comments = data['data']['children']
        new_comments = 0
        pages_parsed = 0
        
        for i, c in enumerate(comments):
            comment = c['data']

            if comment['id'] <= next_newest_id: # comments ids are generated sequentially
                # so we can safely compare them like this without having to cache a timestamp
                # and without risking problems if a comment is deleted
                self.logger.debug("%s: comment['id'] <= next_newest_id" % current_process().name)
                break
            
            # Create new Comment, stick in it in the database.
            # I feel like we should be able to loop through the JSON object and avoid writing out all these assignments
            # Would that even be a good idea?
            comment_entry = Comment()
            comment_entry.subreddit_id           = comment['subreddit_id']
            comment_entry.link_title             = comment['link_title']
            comment_entry.subreddit              = comment['subreddit']
            comment_entry.link_author            = comment['link_author']
            comment_entry.id                     = comment['id']
            comment_entry.gilded                 = comment['gilded']
            comment_entry.author                 = comment['author']
            comment_entry.parent_id              = comment['parent_id']
            comment_entry.body                   = comment['body']
            comment_entry.edited                 = comment['edited']
            comment_entry.author_flair_css_class = comment['author_flair_css_class']
            comment_entry.downs                  = comment['downs']
            comment_entry.body_html              = comment['body_html']
            comment_entry.link_id                = comment['link_id']
            comment_entry.score_hidden           = comment['score_hidden']
            comment_entry.name                   = comment['name']
            comment_entry.created                = datetime.fromtimestamp(comment['created'])
            comment_entry.author_flair_text      = comment['author_flair_text']
            comment_entry.created_utc            = datetime.fromtimestamp(comment['created_utc'])
            comment_entry.ups                    = comment['ups']
            comment_entry.distinguished          = comment['distinguished']
            
            # Append to current session. We'll commit at the end.
            session.add(comment_entry)

            # update our counter
            # For informational purposes. Maybe I'll have it propagate a log in the database,
            #  that would make it really easy to graph comment rate over time           
            new_comments = new_comments + 1
        else:
            # we didn't break out of the loop, therefore we never encountered next_newest_id
            # so, get the next page and keep going
            data, newest_id, after = self._parse_json(url, after)
            
            if pages_parsed <= 3:
                # we should never have to go back further than two additional pages
                # if we have, something is probably wrong            
                self.logger.debug("Getting a second page.")
                pages_parsed = pages_parsed + 1
                self._process_comments(url, next_newest_id, data, after)
            else:
                self.logger.debug("Attempted to parse more than three pages.")

        # Push new objects to database
        session.commit()
        
        self.logger.debug( "%s: %s %s" % (current_process().name, datetime.now(), new_comments) )
        
        # no need to return anything right now
        # return (next_newest_id)

def main():
    # we get cfg_file from models.py
    # see import at the top
    
    username = cfg_file.get('reddit', 'username')
    password = cfg_file.get('reddit', 'password')
    
    print "Logging in..."
    comments = Monitor(username, password)
    print "  Success!"
    
    comments.monitor_comments()


if __name__ == "__main__":
    main()