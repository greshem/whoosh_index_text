# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import sys
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

from jieba.analyse import ChineseAnalyzer


def _index_one_file(file_name, writer):
    with open(file_name,"rb") as inf:
        i=0
        for line in inf:
            i+=1
            try:
                content=line.decode('utf8','ignore')  #注意utf8doc ;
                #content=line.decode('gbk')
                assert  type(content) == unicode
            except Exception, e:
                    return
            file_name= file_name.decode("utf8")
            writer.add_document(
                title="line"+str(i),
                path=file_name,
                content=content, 
                #content=line
            )

def index_one_dir(input_dir, output_index_dir):
    analyzer = ChineseAnalyzer()
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
    if not os.path.exists(output_index_dir):
        os.mkdir(output_index_dir)
    ix = create_in(output_index_dir, schema)
    writer = ix.writer()


    for root,_,files  in  os.walk(input_dir):
        for each in  files:
            abs_path=os.path.join(root,each);
            if abs_path.endswith("txt"):
                print abs_path;
                _index_one_file(abs_path, writer);
    writer.commit()

    print "索引已经生成 位于:%s 目录 "%output_index_dir;


def search_test():
    searcher = ix.searcher()
    parser = QueryParser("content", schema=ix.schema)

    #for keyword in ("水果小姐","你","first","中文","交换机","交换"):

    keyword="配置";
    print "开始查询 关键字: |%s|"%keyword; 

    print("result of " + keyword)
    q = parser.parse(keyword)
    results = searcher.search(q)
    for hit in results:
        print(hit.highlights("content"))
    print("="*10)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_dir = sys.argv[1]
        output_index_dir = sys.argv[2]
        index_one_dir(input_dir, output_index_dir)
    else:
        print "Usage: %s input_dir   output_index_dir";
        sys.exit(-1);


