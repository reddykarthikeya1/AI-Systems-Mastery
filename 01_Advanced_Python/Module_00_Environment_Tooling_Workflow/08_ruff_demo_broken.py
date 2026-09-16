# ==============================================================================
# INTENTIONALLY FLAWED CODE FILE FOR RUFF LINTING AND FORMATTING EXERCISES
#
# Try running:
#   ruff check 02_ruff_demo_broken.py
#   ruff check --fix 02_ruff_demo_broken.py
#   ruff format 02_ruff_demo_broken.py
# ==============================================================================

import os, sys, math  # Multiple imports on single line, unused imports
from collections import *  # Wildcard import
import json

# Flaw 1: Inheriting from object is redundant in Python 3 (UP004)
class UserAccount(object):
    # Flaw 2: Mutable default argument! (B006)
    def __init__(self, username, tags=[]):
        self.username = username
        self.tags = tags

    # Flaw 3: Bad function naming (N802)
    def AddTag(self, new_tag):
        self.tags.append(new_tag)
        return None  # Redundant return None (SIM910 / RET501)

# Flaw 4: Using == None instead of 'is None' (E711)
def check_status(value=None):
    if value == None:
        # Flaw 5: Old-style string formatting (UP031)
        print("Status is empty for: %s" % "Anonymous")
    else:
        # Flaw 6: str.format() instead of f-string (UP032)
        print("Status is active for: {}".format(value))

# Flaw 7: Inconsistent spacing, bad indentation, trailing whitespace
def calculate_metrics( a,b, c ):
    result = (a+b) *c 
    return result

if __name__ == "__main__":
    acc1 = UserAccount("alice")
    acc1.AddTag("admin")
    
    # Bug demonstration with mutable default argument:
    acc2 = UserAccount("bob")
    print("Bob's tags (should be empty):", acc2.tags)  # Prints ['admin'] because of shared mutable default!
    check_status()
