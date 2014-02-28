This scraper was written in Python 2.6.9, but should run under Python 2.7.x.

I recommend you run this in a Python virtualenv, managing the dependencies with `pip` to avoid conflicts.

I also recommend the use of datagrok's `inve` tool for working with virtualenv: https://gist.github.com/datagrok/2199506

# Dependencies

- `httplib2`

- `SQLAlchemy`. May install as a system package or via `pip`. I recommend `pip`.

- A Python database driver for your chosen database engine. E.g. `MySQL-python`. This may install as a system package, or via `pip`.

Other required modules, such as urllib and simplejson, should have shipped with your Python installation.


# Installation

1. Install the dependencies.

2. Create a database using your preferred engine.
   The database needs to have support for full 4-byte Unicode. If you're on PostgreSQL, this is not an issue. If you're on MySQL,
   there's some things you need to make sure are set. See here: http://www.somacon.com/p580.php TL;DR: use `utf8mb4` and `utf8_unicode_ci`.

3. Set up the config file with the correct values for database and reddit account.

       $ mv scraper.cfg.example scraper.cfg

3. Confirm database connectivity and create the database tables.
   Fire up an interactive Python session (`$ python`), import everything from models (`from models import *`), and issue the `create_all()` command to SQLALchemy (`Base.metadata.create_all(engine)`):
   
       $ python
       Python 2.6.9 (unknown, Oct 29 2013, 19:58:13) 
       [GCC 4.6.3 20120306 (Red Hat 4.6.3-2)] on linux2
       Type "help", "copyright", "credits" or "license" for more information.
       >>> from models import *
       >>> Base.metadata.create_all(engine)
       >>> <ctrl-D>

4. Run the scraper: `$ python scrape_comments.py`


# Troubleshooting

- If you run into issues with step 2, you probably have an issue with SQLAlchemy or your database system. Check your connection information and database access permissions.

- If you run into issues like `latin1 codec can't decode byte [...] ordinal not in range [...]`, this means your database system has not been set up to properly handle 4-byte Unicode.
  This probably means you're using MySQL and haven't configured the collation and character set properly. See the link in Step 1.
  
