import sys, os
from ConfigParser import SafeConfigParser

from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


cfg_file = SafeConfigParser()
path_to_cfg = os.path.abspath(os.path.dirname(sys.argv[0]))
path_to_cfg = os.path.join(path_to_cfg, 'scraper.cfg')
cfg_file.read(path_to_cfg)

if cfg_file.get('database', 'system').lower() == 'sqlite':
    engine = create_engine(
        cfg_file.get('database', 'system')+':///'+\
        cfg_file.get('database', 'database'))
else:
    engine = create_engine(
        cfg_file.get('database', 'system')+'://'+\
        cfg_file.get('database', 'username')+':'+\
        cfg_file.get('database', 'password')+'@'+\
        cfg_file.get('database', 'host')+'/'+\
        cfg_file.get('database', 'database')+\
        '?charset=utf8')

# We need multi-byte Unicode support if we're in MySQL.
# Note: MySQL database needs to have everything set up properly for 4-byte UTF-8
# see: http://mathiasbynens.be/notes/mysql-utf8mb4
if cfg_file.get('database', 'system').lower() == 'musql':
    engine.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;")

Base = declarative_base()
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


class Comment(Base):

    """Table containing the comments that have been scraped.

    See line-level comments and reddit JSON documentation: https://github.com/reddit/reddit/wiki/JSON
    """

    __tablename__ = 'comments'

    subreddit_id = Column(String(32), nullable=False) # t5_2qh1i
    link_title = Column(Text, nullable=False) # What brings out the worst in you?
    # banned_by = Column(String(32), nullable) # Name of mod who banned user, if user is banned. Not stored.
    subreddit = Column(String(32), nullable=False) # AskReddit
    link_author = Column(String(32), nullable=False) # k-strike
    # likes = Column() # Whether the comment has been liked by the user. Not stored. null/True/False
    # replies = Column() # Used for messages.
    # saved = Column() # Whether the link or comment has been saved by the user. Not stored. True/False
    id = Column(String(32), nullable=False, primary_key=True) # cfhu3r4
    gilded = Column(Integer, nullable=False, default=0) # No. of times gilded.
    author = Column(String(32), nullable=False) # username
    parent_id = Column(String(32), nullable=False) # ID of parent. Either the link id (if top level comment) or another comment id. E.g. "t3_1y52yc"
    # approved_by = Column(String(32)) # Username of mod who approved comment. Not stored. null/String
    body = Column(Text, nullable=False, default="") # Unprocessed Markdown source of comment text. 
    edited = Column(Boolean, nullable=False, default=False) # Has comment been edited? True/False
    author_flair_css_class = Column(Text, nullable=True) # How long can this even be?
    downs = Column(Integer, nullable=False, default=0) # No. downvotes.
    body_html = Column(Text, nullable=False, default="") # Processed HTML of comment text.
    link_id = Column(String(32), nullable=False) # thing_id of the submission the comment is attached to.
    score_hidden = Column(Boolean, default=False) # Whether the score has been hidden.
    name = Column(String(32), nullable=False) # Full thing_id of comment. E.g. "t1_cfhu3r4"
    created = Column(DateTime, nullable=False) # Local time. Local to reddit, or local to API client? Do we even need this? Either way it's PST. API spits out 'long's, but we convert to datetime.datetime().
    author_flair_text = Column(Text, nullable=True) # How long can this be? Usually going to be null.
    created_utc = Column(DateTime) # UTC time. See comment on `created`
    ups = Column(Integer, nullable=False, default=0) # No. upvotes
    # num_reports = Column(Integer, nullable=True) # Not stored.
    distinguished = Column(Enum("moderator", "admin", "special", name="distinguish_types"), nullable=True) # see http://bit.ly/ZYI47B
    

# class Log(Base):
#     """Table containing a log of the bot's actions."""
# 
#     __tablename__ = 'log'
# 
#     id = Column(Integer, primary_key=True)
#     item_fullname = Column(String(255), nullable=False)
#     action = Column(Enum('approve',
#                          'remove',
#                          'report',
#                          'link_flair',
#                          'user_flair',
#                          name='log_action'))
#     condition_yaml = Column(Text)
#     datetime = Column(DateTime)

