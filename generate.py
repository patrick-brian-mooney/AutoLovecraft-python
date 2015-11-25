#! /usr/bin/env python


# NEVER edit this version of the script directly.


"""Script to post to AutoLovecraft.tumblr.com. Really rough sketch of a
script here. Not really meant for public use. Based on my earlier script to
do a similar job for the IrishLitDiscourses Tumblr account; see
https://github.com/patrick-brian-mooney/IrishLitDiscourses-python

The fact that there isn't real documentation here is intentionally meant to
reinforce that this is a rough draft not meant for public use. Use at your own
risk. My hope is that this script is helpful, but I explicitly disclaim ANY
RESPONSIBILITY for the behavior of this piece of work. If you don't have the
expertise to evaluate its risks, it's not for you. To put it more bluntly: THIS
SOFTWARE IS OFFERED WITHOUT WARRANTY OF ANY KIND AT ALL.
"""


# Thanks to https://epicjefferson.wordpress.com/2014/09/28/python-to-tumblr/ for first steps here

import random
import pprint
import subprocess

import pytumblr

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library

# Set up default values
patrick_logger.verbosity_level = 2

# Functions

def print_usage():    # Note that, currently, nothing calls this.
    """Print the docstring as a usage message to stdout"""
    patrick_logger.log_it("INFO: print_usage() was called")
    print(__doc__)

# OK, set up the constants we'll need.
the_client = pytumblr.TumblrRestClient(
  'FILL ME IN',  #consumer_key
  'FILL ME IN',  #consumer_secret
  'FILL ME IN',  #token_key
  'FILL ME IN'  #token_secret
)

patrick_logger.log_it("INFO: Tumblr authentication constants set up, starting run ...", 2)

# Next, pick out a title between 10 and 70 characters
the_length = 300
patrick_logger.log_it("INFO: getting a story title ...", 2)
while not 10 <= the_length <= 70:
    the_title = subprocess.check_output(["dadadodo -c 1 -l /lovecraft/chains.dat -w 10000"], shell=True).strip()
    the_length = len(the_title)
    patrick_logger.log_it("INFO: The story title generated was '" + the_title + ".'", 2)
    patrick_logger.log_it("INFO:    And the length of that title is: " + str(the_length), 2)
    if the_title in open('/lovecraft/titles.txt').read():    # Incidentally, this is a really bad idea if the log of titles ever gets very big
        patrick_logger.log_it("That title's been used! Trying again ...\n\n\n")
        the_length = 300    # Force the loop to grind through again
    else:
        patrick_logger.log_it("   That's a new title!", 2)

patrick_logger.log_it("OK, we've got a title.\n\n", 2)

the_blog_name = "AutoLovecraft"
normal_tags = ['H.P. Lovecraft', 'automatically generated text', 'Patrick Mooney', 'dadadodo']
temporary_tags = ['The Call of Cthulhu', '1928', 'The Call of Cthulhu week']
story_length = random.choice(list(range(25, 55)))
the_content = ''

patrick_logger.log_it('INFO: tags are:' + pprint.pformat(normal_tags + temporary_tags), 2)
patrick_logger.log_it('INFO: requested story length is: ' + str(story_length) + ' sentences ... generating ...', 2)

the_content = subprocess.check_output(["dadadodo -c " + str(story_length) + " -l /lovecraft/chains.dat -w 10000"], shell=True)
the_content = the_content.strip()

# All right, we're ready. Let's go.
patrick_logger.log_it('INFO: Attempting to post the content', 2)
the_status = the_client.create_text(the_blog_name, state="published", tags=normal_tags + temporary_tags, title=the_title, body=the_content)
patrick_logger.log_it('INFO: the_status is: ' + pprint.pformat(the_status), 2)

try:
    patrick_logger.log_it('INFO: Adding title of that post to list of titles', 2)
    open('/lovecraft/titles.txt', 'a').write(the_title + '\n')
except IOError:
    patrick_logger.log_it("ERROR: Can't add the title to the list of used titles.", 0)

patrick_logger.log_it('INFO: We\'re done', 2)
