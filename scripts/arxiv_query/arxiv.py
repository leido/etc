#!/usr/bin/env python3
#coding = utf-8

import feedparser
import sys
# from enum import Enum

# class QueryPrefix(Enum):
#     ALL = 'all'
#     TITLE = 'ti'
#     AUTHOR = 'au'
#     ABSTRACT = 'abs'
#     COMMENT = 'co'
#     JOURNAL = 'jr'
#     CATEGORY = 'cat'
#     NUMBER = 'rn'
#     # id is not sure, so not included



class Article(object):
    """
    Simple wrapper for feed item e.g. one article retrieved
    """
    def __init__(self, item):
        self.title = None
        self.category = None
        self.published = None
        self.updated = None
        self.summary = None

        self.set_attr(item)

    def set_attr(self, item):
        self.title = item['title']
        self.category = item['arxiv_primary_category']['term']
        self.summary = item['summary']
        self.published = item['published']
        self.updated = item['updated']
    
    def get_category(self):
        return self.category

    def get_short(self):
        return 'title:{}\npub:{}\n'.format(self.title, self.published)
    def __str__(self):
        strings = ('title: ' + self.title, 
                   'category: ' + self.category,
                   'published: ' + self.published, 
                   'updated: ' + self.updated,
                   'summary: ' + self.summary)
        return '\n'.join(strings) + '\n'


def vprint(obj):
    strings = ('title: ' + obj.title,
               'category: ' + obj.category,
               'published: ' + obj.published,
               'updated: ' + obj.updated,
               'summary: ' + obj.summary)
    print('\n'.join(strings)+ '\n')


def sprint(obj):
    strings = 'title: ' + obj.title + '\n' + 'category: ' + obj.category + '\n' + 'published: ' + obj.published + '\n'
    print(strings)


def get_url(phrase, prefix='all', start=0, max_results=10, sort_by='relevance', sort_order='descending'):
    """
    Return query url for feedparser

    Args:
    `prefix` is one of the following:
    |------------------------------------|
    |    prefix | explanation            |
    |------------------------------------|
    |    ti 	| Title                  |
    |    au 	| Author                 |
    |    abs    | Abstract               |
    |    co 	| Comment                |
    |    jr 	| Journal Reference      |
    |    cat    | Subject Category       |
    |    rn 	| Report Number          |
    |    id 	| Id(use id_list instead)|
    |    all    | All of the above       |
    |------------------------------------|
    `sort_by` can be "relevance", "lastUpdatedDate", "submittedDate"
    `sort_order` can be either "ascending" or "descending"

    Returns:
    url to parse
    """
    base_url = 'http://export.arxiv.org/api/query?search_query='
    url =  base_url + \
           prefix+':'+phrase + \
           '&start='+str(start) + \
           '&max_results='+str(max_results) + \
           '&sortBy='+sort_by + \
           '&sortOrder='+sort_order
    return url


def url_update(url):
    """
    Update url `start` entry
    """
    url_lst = url.split('&')
    start_str = url_lst[1]
    max_results_str = url_lst[2]
    idx1, idx2 = start_str.find('='), max_results_str.find('=')
    num1, num2 = int(start_str[idx1+1:]), int(max_results_str[idx2+1:])
    url_lst[1] = 'start=' + str(num1+num2)
    return '&'.join(url_lst)


def _query_base(url):
    # print(url)
    results = feedparser.parse(url)
    if results['status'] != 200:
        raise Exception("HTTP Error " + str(results['status']) + ' in query')
    else:
        results = results['entries']

    return [Article(i) for i in results]



def query(url, num):
    interests = ['cs.CV', 'cs.LG', 'cs.AI', 'cs.HC', 'cs.MM']
    interest_articles = []
    idx = 0
    while idx < num:
        articles = _query_base(url)
        for i in articles:
            if i.get_category() in interests:
                interest_articles.append(i)
                idx += 1
                if idx == num:
                    break
        url = url_update(url)
    return interest_articles

        

def main(keyword='residual',func='v', num=3):
    url = get_url(keyword, prefix='ti', sort_by='submittedDate')
    articles = query(url, int(num))
    for i in articles:
        if func == 'v':
            vprint(i)
        elif func == 's':
            sprint(i)
        

if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
