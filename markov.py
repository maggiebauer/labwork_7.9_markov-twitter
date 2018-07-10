"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Take list of files. Open them, read them, and return one long string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Take dictionary of Markov chains; return random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    while len(" ".join(words)) <= 140:    
        while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text).
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.
            word = choice(chains[key])
            words.append(word)
            key = (key[1], word)

    return " ".join(words)


def tweet(chains):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
    
    print(api.VerifyCredentials())

    status = api.PostUpdate(chains)
    print(status.text)   


    tweeting = True
    while tweeting:
        keep_tweeting = input('Enter to tweet again [q to quit] > ')
        if keep_tweeting == '\n':

            print(api.VerifyCredentials())

            status = api.PostUpdate(chains)
            print(status.text)
        elif keep_tweeting.lower().strip() == 'q':
            tweeting = False
        else:
            print('I didn\'t understand that. Please try again.')
            continue



# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)


# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)
chains_2 = make_text(chains)
tweet(chains_2)
