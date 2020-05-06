#!/usr/bin/env python3.5
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

# Thanks to https://epicjefferson.wordpress.com/2014/09/28/python-to-tumblr/
for first steps here when I was first cutting my teeth on Python.
"""



import bz2
import datetime
import json
import os
import pprint
import random
import sys

import social_media                 # From https://github.com/patrick-brian-mooney/personal-library
from social_media_auth import autolovecraft_client

import text_generator as tg         # https://github.com/patrick-brian-mooney/markov-sentence-generator



# First, some contants.
chains_file = '/lovecraft/corpora/Memory.2.pkl'
post_archives = '/lovecraft/archives'

the_tags = ['H.P. Lovecraft', 'automatically generated text', 'Patrick Mooney', 'Python',
            'Markov chains', '1919', 'Memory', 'Memory week']


# Utility functions
def print_usage():    # Note that, currently, nothing calls this.
    """Print the docstring as a usage message to stdout"""
    print("INFO: print_usage() was called")
    print(__doc__)


if __name__ == "__main__":
    story_length = random.choice(list(range(25, 71)))
    the_content = ''

    print("INFO: tags and sentence lengths set up ...")
    genny = tg.TextGenerator(name='Lovecraft Generator')
    genny.chains.read_chains(chains_file)
    print("INFO: chains read, starting run ...")

    # Next, pick out a title between 10 and 70 characters
    print("INFO: getting a story title ...")
    the_title = 'herp a derp!' * 50             # pick something much too long.
    previous_titles = open('/lovecraft/titles.txt').read()
    tries, max_length = 0, 70

    while not 10 <= len(the_title) <= max_length:
        the_title = genny.gen_text().strip()
        tries += 1
        title_length = len(the_title)
        print("INFO: The story title generated was '%s'" % the_title)
        print("INFO:    And the length of that title is: %d" % len(the_title))
        if the_title in previous_titles:
            print("That title's been used! Trying again ...\n\n\n")
            continue
        else:
            print("   That's a new title!")
            if len(the_title) > max_length:
                tries += 1
                if tries % 100 == 0:    # Every hundred failed titles, bump up maximum allowed title length.
                    max_length += 1     # hopefully, this means we'll eventually find a legal title.

    print("OK, we've got a title.\n\n")

    print('INFO: tags are:' + pprint.pformat(the_tags))
    print('INFO: requested story length is: ' + str(story_length) + ' sentences ... generating ...')

    the_content = genny.gen_text(sentences_desired=story_length, paragraph_break_probability=0.2)
    the_lines = ["<p>" + the_line.strip() + "</p>" for the_line in the_content.split('\n\n')]
    print("the_lines: " + pprint.pformat(the_lines))
    the_content = "\n\n".join(the_lines)
    print("the_content: \n\n" + the_content)

    # All right, we're ready. Let's go.
    print('INFO: Attempting to post the content')
    the_status, the_tumblr_data = social_media.tumblr_text_post(autolovecraft_client, the_tags, the_title, the_content)
    print('INFO: the_status is: ' + pprint.pformat(the_status))
    print('INFO: the_tumblr_data is: ' + pprint.pformat(the_tumblr_data))

    try:
        print('INFO: Adding title of that post to list of titles')
        with open('/lovecraft/titles.txt', 'a') as f:
            f.write(the_title + '\n')
    except IOError:
        print("ERROR: Can't add the title to the list of used titles.", 0)

    # Keep an archived copy
    post_data = {'title': the_title, 'text': the_content, 'time': datetime.datetime.now().isoformat() }
    post_data['formatted_text'], post_data['tags'] = the_lines, the_tags
    post_data['status_code'], post_data['tumblr_data'] = the_status, the_tumblr_data
    archive_name = "%s — %s.json.bz2" % (the_status['id'], the_title)
    with bz2.BZ2File(os.path.join(post_archives, archive_name), mode='wb') as archive_file:
        archive_file.write(json.dumps(post_data, sort_keys=True, indent=3, ensure_ascii=False).encode())

    print("INFO: We're done")

    print("Cythonized? {}".format(tg._is_cythonized()))

    print("Ran under Python version: " + sys.version)
