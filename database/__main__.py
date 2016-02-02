""" Database viewer
"""

import shelve
import database

shelf = shelve.open(database.filename, flag='r')
print repr(shelf)
shelf.close()