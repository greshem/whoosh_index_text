# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import sys
reload(sys);
sys.setdefaultencoding("utf-8")  

import sys
import os
sys.path.append("../")
from whoosh.index import create_in
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

import sys, os



def chomp(line):
    if line[-1] == '\n':
        line = line[:-1]
    return line;

def search_index(index_dir, keyword):
    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists(index_dir):
        raise(" dir not exist");

    print "使用 索引目录 %s"%index_dir;
    ix = open_dir(index_dir)
    searcher = ix.searcher()
    parser = QueryParser("content", schema=ix.schema)

    #utf8_str=unicode(gb2312_str, 'gb2312');
    keyword=unicode(str(keyword));
    print(keyword);

    print("result of " + keyword)
    q = parser.parse(keyword)
    #results = searcher.search(query,limit=20). 若要得到全部的结果，可把limit=None.
    results = searcher.search(q,limit=100)
    count=0
    for hit in results:
        count+=1
        print "#===================================";
        print "count=%s"%count;
        print "%s|%s"%(hit["path"], hit["title"])
        print  chomp(hit["content"])

if __name__ == '__main__':

    if len(sys.argv) == 3:
        search_index(sys.argv[1], sys.argv[2])
    else:
        print "Usage: %s input_index_dir   keyword";
        sys.exit(-1);

