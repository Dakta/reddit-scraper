# Reddit Scraper

This is a fairly simple multi-threaded reddit comment scraper and parser written in Python.
I do not recommend using this code unmodified in any environment, particularly not production.

Roughtly based on MetaReddit and AutoModerator.

This is tested with Python 2.6.9.

You will need SQLAlchemy and a python driver module for your database engine (e.g. MySQL-python).

# Setup

1. Create a database using your preferred engine. Set up the config file with the correct values for database and reddit account.
   The database needs to have support for full 4-byte Unicode. If you're on PostgreSQL, this is no big deal. If you're on MySQL,
   there's some things you need to make sure are set. See here: http://www.somacon.com/p580.php TL;DR: use `utf8mb4` and `utf8_unicode_ci`.

2. `cd` to the main project directory. Fire up an interactive Python session (`$ python`), import everything from models (`from models import *`), and issue the `create_all()` command to SQLALchemy (`Base.metadata.create_all(engine)`):
    $ python
    Python 2.6.9 (unknown, Oct 29 2013, 19:58:13) 
    [GCC 4.6.3 20120306 (Red Hat 4.6.3-2)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from models import *
    >>> Base.metadata.create_all(engine)

3. Run the scraper: `$ python scrape_comments.py`

If you run into issues with step 2, you probably have an issue with SQLAlchemy or your database system. Check your connection information and database access permissions.

