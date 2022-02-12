#!/usr/bin/env python3

import bibtexparser
import logging
import re
import sys

'''
Read a bibtex file as named by parameter, and transform a document on stdin to stdout while replacing citations.

Specifically:

- Replace strings of the form "[http:]cite:[...]" with a url from the given bibtex entry.
- Replace strings of the form "(-|--|---|—) cite:[…]" with a templated HTML block based on the citation's data
'''

def init_logging():
    log = logging.getLogger()
    # log.setLevel(logging.DEBUG)
    # log.setLevel(logging.WARN)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)


class Transformer (object):
    def __init__(self, *args, **kwargs):
        self._bib = kwargs['bibtex']
        self._input = list(kwargs['lines_in'])
        self._output = []
        self._log = logging.getLogger('Transformer')
        #
        self.process()

    def _contains_citation(self, line):
        return line.find('cite:') >= 0

    _cite_patterns = re.compile(r'''(http:|(&#x2014;|—|–|-+)\s*)?cite:([^ <"]+)''')
    def _expand_citation(self, line_no, line):
        res = self._cite_patterns.search(line)
        if res:
            full_match,prefix,cite_ref = res.group(0),res.group(1),res.group(3)
            cite_ref = cite_ref.rstrip()
            cite = self._bib.entries_dict.get(cite_ref)
            self._log.debug(f'prefix [{prefix}] cite_ref [{cite_ref}] cite [{cite}] line_no [{line_no}]')
            if cite:
                # assert(cite != null)
                if prefix == 'http:': # and 'url' in cite.keys():
                    replacement = cite['url']
                else:
                    # prefix must be dashes
                    try:
                        replacement = f'''<p><cite><a data-cite="{cite_ref}" href="{cite['url']}">— {cite['author']}, {cite['date']}</a></cite></p>'''
                    except KeyError as e:
                        self._log.error(f'key error for citation [{cite_ref}]', e)
                try:
                    line = line.replace(full_match, replacement)
                except UnboundLocalError as ule:
                    self._log.error(f'for cite [{cite_ref}] on line_no [{line_no}]', ule)
            else:
                self._log.error(f'citation [{cite_ref}] finds no bib entry; skipping expansion')
        return line

    def process(self):
        i = 0
        for line in self._input:
            i = i + 1
            while self._contains_citation(line):
                pre = line
                post = self._expand_citation(i, pre)
                if pre == post:
                    self._log.error(f'ERR pre [{pre}] == post [{post}]')
                    break
                line = post
            else:
                # line is line is line
                pass
            #
            self._output.append(line)

    @property
    def output(self):
        return self._output

if __name__ == '__main__':
    init_logging()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--bibtex', help='bibtex file to parse', default='guide.bib')
    parsed_args = parser.parse_args()
    bibtex_filename = parsed_args.bibtex
    bib = None
    try:
        with open(bibtex_filename) as bibtex_file:
            bib = bibtexparser.load(bibtex_file)
    except Error as e:
        raise Execption(f'attempting to parse bibtex input [{bibtex_filename}]', e)

    input = sys.stdin
    t = Transformer(bibtex=bib, lines_in=input)
    for line in t.output:
        print(line.rstrip())
    pass

