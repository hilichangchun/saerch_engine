import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, request, render_template, redirect, url_for
from config import Config #initialize_application_config
import pymysql
from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from indexer import *
from recommender import *

from searcher_v2 import *
import random
import time


app = Flask(__name__)


def load_glove():
    """
    load glove pre-trained word vectors
    :return: Glove model
    """

    # data path has to be absolute path
    glove_file = datapath(r'/Users/changchun/PycharmProjects/news_search/glove.6B.100d.txt')
    word2vec_glove_file = get_tmpfile("glove.6B.100d.word2vec.txt")
    glove2word2vec(glove_file, word2vec_glove_file)
    glove_model = KeyedVectors.load_word2vec_format(word2vec_glove_file)
    return glove_model


@app.route('/')
def main():


    target1 = 'Business'
    target2 = 'Entertainment'
    target3 = 'Health'
    target4 = 'Politics'
    target5 = 'Sci_Tech'
    target6 = 'Sport'
    target7 = 'World'

    db = pymysql.connect("dbforedinburgh.cqpftfdbw3kd.eu-west-2.rds.amazonaws.com", "admin", "ttds2020",
                         "TTDS_onlineCrawler")
    cursor = db.cursor()
    select_str = 'SELECT ID FROM category WHERE NAME = %s'
    select_str2 = 'SELECT a.ID, a.TITLE, a.AUTHOR, a.DATE, a.IMAGE, a.URL FROM docSummary a INNER JOIN docCategory b ON a.ID = b.ID WHERE b.CATE_ID = %s ORDER BY a.DATE DESC LIMIT 10'

    cursor.execute(select_str, target1)
    sulin1 = cursor.fetchone()
    cursor.execute(select_str2, sulin1[0])
    # INDEX: 0->documentID, 1->TITLE, 2->AUTHOR, 3->DATE, 4->IMAGE, 5->URL
    sulin1 = cursor.fetchall()

    cursor.execute(select_str, target2)
    sulin2 = cursor.fetchone()
    cursor.execute(select_str2, sulin2[0])
    # INDEX: 0->documentID, 1->TITLE, 2->AUTHOR, 3->DATE, 4->IMAGE, 5->URL
    sulin2 = cursor.fetchall()

    cursor.execute(select_str, target3)
    sulin3 = cursor.fetchone()
    cursor.execute(select_str2, sulin3[0])
    # INDEX: 0->documentID, 1->TITLE, 2->AUTHOR, 3->DATE, 4->IMAGE, 5->URL
    sulin3 = cursor.fetchall()

    cursor.execute(select_str, target4)
    sulin4 = cursor.fetchone()
    cursor.execute(select_str2, sulin4[0])
    # INDEX: 0->documentID, 1->TITLE, 2->AUTHOR, 3->DATE, 4->IMAGE, 5->URL
    sulin4 = cursor.fetchall()

    cursor.execute(select_str, target5)
    sulin5 = cursor.fetchone()
    cursor.execute(select_str2, sulin5[0])
    # INDEX: 0->documentID, 1->TITLE, 2->AUTHOR, 3->DATE, 4->IMAGE, 5->URL
    sulin5 = cursor.fetchall()

    cursor.execute(select_str, target6)
    sulin6 = cursor.fetchone()
    cursor.execute(select_str2, sulin6[0])
    # INDEX: 0->documentID, 1->TITLE, 2->AUTHOR, 3->DATE, 4->IMAGE, 5->URL
    sulin6 = cursor.fetchall()

    cursor.execute(select_str, target7)
    sulin7 = cursor.fetchone()
    cursor.execute(select_str2, sulin7[0])
    # INDEX: 0->documentID, 1->TITLE, 2->AUTHOR, 3->DATE, 4->IMAGE, 5->URL
    sulin7 = cursor.fetchall()
    db.close()

    return render_template('search_index.html', sulin1 = sulin1, sulin2 = sulin2, sulin3 = sulin3, sulin4 = sulin4, sulin5 = sulin5, sulin6 = sulin6, sulin7 = sulin7)

"""@app.route('/articles/show')
def show_article():
    url_to_clean = request.args.get('url_to_clean')
    if not url_to_clean:
        return redirect(url_for('layout.html'))
        """


@app.route('/search/')
def search():
    time_start = time.time()
    flag = True
    search_instance = SearchModule()
    #glove_model = load_glove()
    #search_instance.get_glove_model(glove_model)

    while flag == True:
        # todo: interface of getting search query here
        global query
        global search_results
        global lens

        query = request.args.get('query')

        #time_start = time.time()

        if query == 'wibiwibiwibibabo':
            flag = False
        else:
            search_instance.get_search_query(query)
            search_results, lens = search_instance.conduct_search()
            time_end = time.time()
            #print('search time cost', time_end - time_start, 's')
            #print('search result: ' + str(search_results) + '    number of news found: ' + str(lens))
            #similar_comb = search_instance.find_similar_search_comb()
            #print(similar_comb)
            #pages = []
            #for i in range(1, lens // 10 + 1):
            #    pages.append(i)
            if not search_results:
                return no_results_template(query)
            #db = pymysql.connect("dbforedinburgh.cqpftfdbw3kd.eu-west-2.rds.amazonaws.com", "admin", "ttds2020",
            #                       "TTDS_onlineCrawler")
            #cursor = db.cursor()
            #cursor.execute('SELECT * FROM `docSummary` where ID in (%s) LIMIT 10 OFFSET 0' % ','.join(['%s'] * len(search_results)), search_results)
            #sulin = cursor.fetchall()
            #db.close()
            print(query)
            login_url = '/search/page/1/'
            return redirect(login_url)
            #return render_template('search_results.html',article = sulin,pages=pages, ID=search_results, query=query, lens=lens,  error=True)




@app.route('/search/page/<int:page>/', methods=['GET', 'POST'])
def next(page):

        perpage = 10
        startat = (page-1) * perpage
        pages = []

        for i in range(1, lens // 10 + 1):
            pages.append(i)
        search_results2 = search_results[startat:startat + perpage]
        db = pymysql.connect("dbforedinburgh.cqpftfdbw3kd.eu-west-2.rds.amazonaws.com", "admin", "ttds2020",
                                "TTDS_onlineCrawler")
        cursor = db.cursor()
        target = []
        for i in search_results2:
            select_str = 'SELECT a.*, b.CATE_ID FROM docSummary a INNER JOIN docCategory b ON a.ID = b.ID WHERE a.ID = %s'
            cursor.execute(select_str,i)
            sulin = cursor.fetchone()
            target.append(sulin)
        target = tuple(target)
        db.close()
        return render_template('search_results.html', article=target, pages=pages, ID=search_results, query=query, lens=lens, error=True)


@app.route('/search/article/<id>/', methods=['GET', 'POST'])
def content(id):
    db = pymysql.connect("dbforedinburgh.cqpftfdbw3kd.eu-west-2.rds.amazonaws.com", "admin", "ttds2020",
                         "TTDS_onlineCrawler")
    cursor = db.cursor()
    select_str = 'SELECT a.*, b.CATE_ID FROM docMainText a INNER JOIN docCategory b ON a.ID = b.ID WHERE a.ID = %s'
    cursor.execute(select_str, id)
    sulin3 = cursor.fetchall()
    sulin3 = sulin3[0]
    select_str = 'SELECT * FROM `recommendationList` where ID = %s'
    cursor.execute(select_str, id)
    sulin1 = cursor.fetchall()
    #print(sulin3)
    temp = sulin1[0][1]
    referID = temp.split(',')
    referID = list(map(int, referID))
    #print(referID)
    targetList = []
    for i in referID:
        select_str = 'SELECT * FROM `docSummary` where ID = %s'
        cursor.execute(select_str, i)
        sulin4 = cursor.fetchone()
        targetList.append(sulin4)
    sulin2 = tuple(targetList)
    db.close()
    #print(sulin3)
    return render_template('news_content.html', id=id, article=sulin3, article2=sulin2)



@app.route('/search/lucky')
def search_lucky():
    luck_num = random.randint(0,169145)
    return redirect('/search/article/luck_num/')


def no_results_template(query):
    return render_template('simple_message.html', title='No results found',
                           message='Your search - <b>' + query + '</b> - Sorry, no result'
                                                             
                                                                 '<li><a href="/">check here to return.</a></ul>')

@app.route('/reset_config')
def reset_config():
    #initialize_application_config()
    return render_template('simple_message.html', title='Application config updated', message='Config attributes: <br>' + str(vars(Config)))



if __name__ == '__main__':
    app.run(debug=True)
