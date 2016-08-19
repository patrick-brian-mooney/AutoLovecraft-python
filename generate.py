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

import random, pprint, subprocess, sys

import patrick_logger    # From https://github.com/patrick-brian-mooney/personal-library
import social_media      # From https://github.com/patrick-brian-mooney/personal-library
from social_media_auth import autolovecraft_client


sys.path.append('/lovecraft/markov_sentence_generator/')
from sentence_generator import *                            # https://github.com/patrick-brian-mooney/markov-sentence-generator

# Set up default values
normal_tags = 'H.P. Lovecraft, automatically generated text, Patrick Mooney, Python, Markov chains,'
temporary_tags = 'Dagon, 1917, Dagon week'
story_length = random.choice(list(range(30, 70)))
the_content = ''

patrick_logger.verbosity_level = 2
chains_file = '/lovecraft/chains.dat'

# Utility functions
def print_usage():    # Note that, currently, nothing calls this.
    """Print the docstring as a usage message to stdout"""
    patrick_logger.log_it("INFO: print_usage() was called")
    print(__doc__)

patrick_logger.log_it("INFO: tags and sentence lengths set up ...", 2)

the_markov_length, the_starts, the_mapping = read_chains(chains_file)

patrick_logger.log_it("INFO: chains read, starting run ...", 2)

# Next, pick out a title between 10 and 70 characters
the_length = 300
patrick_logger.log_it("INFO: getting a story title ...", 2)
while not 10 <= the_length <= 70:
    the_title = gen_text(the_mapping, the_starts, markov_length=the_markov_length, sentences_desired=1, paragraph_break_probability=0).strip()
    the_length = len(the_title)
    patrick_logger.log_it("INFO: The story title generated was '" + the_title + ".'", 2)
    patrick_logger.log_it("INFO:    And the length of that title is: " + str(the_length), 2)
    if the_title in open('/lovecraft/titles.txt').read():    # Incidentally, this is a really bad idea if the log of titles ever gets very big
        patrick_logger.log_it("That title's been used! Trying again ...\n\n\n")
        the_length = 300                                                            # Force the loop to grind through again
    else:
        patrick_logger.log_it("   That's a new title!", 2)

patrick_logger.log_it("OK, we've got a title.\n\n", 2)

patrick_logger.log_it('INFO: tags are:' + pprint.pformat(normal_tags + temporary_tags), 2)
patrick_logger.log_it('INFO: requested story length is: ' + str(story_length) + ' sentences ... generating ...', 2)

the_content = gen_text(the_mapping, the_starts, markov_length=the_markov_length, sentences_desired=story_length, paragraph_break_probability=0.2)
the_lines = ["<p>" + the_line.strip() + "</p>" for the_line in the_content.split('\n\n')]
patrick_logger.log_it("the_lines: " + pprint.pformat(the_lines), 2)
the_content = "\n\n".join(the_lines)
patrick_logger.log_it("the_content: \n\n" + the_content)

# All right, we're ready. Let's go.
patrick_logger.log_it('INFO: Attempting to post the content', 2)
the_status = social_media.tumblr_text_post(autolovecraft_client, normal_tags + temporary_tags, the_title, the_content)
patrick_logger.log_it('INFO: the_status is: ' + pprint.pformat(the_status), 2)

try:
    patrick_logger.log_it('INFO: Adding title of that post to list of titles', 2)
    open('/lovecraft/titles.txt', 'a').write(the_title + '\n')
except IOError:
    patrick_logger.log_it("ERROR: Can't add the title to the list of used titles.", 0)

patrick_logger.log_it('INFO: We\'re done', 2)
