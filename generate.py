#! /usr/bin/env python3
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

import random, pprint, json, bz2, os, datetime 

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library
import social_media      # From https://github.com/patrick-brian-mooney/personal-library
from social_media_auth import autolovecraft_client

import text_generator as tg         # https://github.com/patrick-brian-mooney/markov-sentence-generator


patrick_logger.verbosity_level = 2
chains_file = '/lovecraft/corpora/The Hound.2.pkl'
post_archives = '/lovecraft/archives'

# Set up default values
with open('/lovecraft/current-tags') as tagfile:
    the_tags = ', '.join([t.strip() for t in tagfile.readlines()])

story_length = random.choice(list(range(25, 71)))
the_content = ''


# Utility functions
def print_usage():    # Note that, currently, nothing calls this.
    """Print the docstring as a usage message to stdout"""
    patrick_logger.log_it("INFO: print_usage() was called")
    print(__doc__)

patrick_logger.log_it("INFO: tags and sentence lengths set up ...", 2)

genny = tg.TextGenerator(name='Lovecraft Generator')
genny.chains.read_chains(chains_file)

patrick_logger.log_it("INFO: chains read, starting run ...", 2)

# Next, pick out a title between 10 and 70 characters
the_length = 300
patrick_logger.log_it("INFO: getting a story title ...", 2)
while not 10 <= the_length <= 70:
    the_title = genny.gen_text().strip()
    the_length = len(the_title)
    patrick_logger.log_it("INFO: The story title generated was '%s'" % the_title, 2)
    patrick_logger.log_it("INFO:    And the length of that title is: " + str(the_length), 2)
    if the_title in open('/lovecraft/titles.txt').read():
        patrick_logger.log_it("That title's been used! Trying again ...\n\n\n")
        the_length = 300                                                            # Force the loop to grind through again
    else:
        patrick_logger.log_it("   That's a new title!", 2)

patrick_logger.log_it("OK, we've got a title.\n\n", 2)

patrick_logger.log_it('INFO: tags are:' + pprint.pformat(the_tags), 2)
patrick_logger.log_it('INFO: requested story length is: ' + str(story_length) + ' sentences ... generating ...', 2)

the_content = genny.gen_text(sentences_desired=story_length, paragraph_break_probability=0.2)
the_lines = ["<p>" + the_line.strip() + "</p>" for the_line in the_content.split('\n\n')]
patrick_logger.log_it("the_lines: " + pprint.pformat(the_lines), 2)
the_content = "\n\n".join(the_lines)
patrick_logger.log_it("the_content: \n\n" + the_content)

# All right, we're ready. Let's go.
patrick_logger.log_it('INFO: Attempting to post the content', 2)
the_status, the_tumblr_data = social_media.tumblr_text_post(autolovecraft_client, the_tags, the_title, the_content)
patrick_logger.log_it('INFO: the_status is: ' + pprint.pformat(the_status), 2)
patrick_logger.log_it('INFO: the_tumblr_data is: ' + pprint.pformat(the_tumblr_data), 2)

try:
    patrick_logger.log_it('INFO: Adding title of that post to list of titles', 2)
    with open('/lovecraft/titles.txt', 'a') as f:
        f.write(the_title + '\n')
except IOError:
    patrick_logger.log_it("ERROR: Can't add the title to the list of used titles.", 0)

# Keep an archived copy
post_data = {'title': the_title, 'text': the_content, 'time': datetime.datetime.now().isoformat() }
post_data['formatted_text'], post_data['tags'] = the_lines, the_tags
post_data['status_code'], post_data['tumblr_data'] = the_status, the_tumblr_data
archive_name = "%s — %s.json.bz2" % (the_status['id'], the_title)
with bz2.BZ2File(os.path.join(post_archives, archive_name), mode='wb') as archive_file:
    archive_file.write(json.dumps(post_data, sort_keys=True, indent=3, ensure_ascii=False).encode())

patrick_logger.log_it("INFO: We're done", 2)
