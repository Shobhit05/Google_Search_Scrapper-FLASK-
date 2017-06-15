from flask import Flask, render_template, request, url_for
import re
import requests
from bs4 import BeautifulSoup
import nltk


app = Flask(__name__, static_url_path = "", static_folder = "tmp")


@app.route('/')
def form():
    return render_template('index.html')



@app.route('/result/', methods=['POST'])
def result():
    name=request.form['yourname']
    result=fetch_result(name)
    entity=getnnpentity(result)
    entity=list(set(entity))
    return render_template('result.html', result=result,entity=entity)




def fetch_result(name):
    url="https://www.google.com/search?q="+name
    page = requests.get(url)
    soup = BeautifulSoup(page.text,"lxml")
    links = soup.findAll("a")
    c=[]
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        x=""
        try:
            for i in link.contents:
                if str(i).startswith("<"):
                    a=str(i)
                    x=x+re.sub('<[^>]*>', '', a)
                elif i =="Cached":
                    continue
                else:
                    x=x+str(i)
            if x!="":
                c.append(x)
        except:
            continue
    return c

def getnnpentity(contentArray):
    nnpentity=[]
    try:
        for item in contentArray:
            tokenized = nltk.word_tokenize(item)
            tagged = nltk.pos_tag(tokenized)
            for i in tagged:
                if i[1]=='NNP' and i[0]!='|':
                    nnpentity.append(i)
            namedEnt = nltk.ne_chunk(tagged)
            

    except Exception, e:
        print str(e)
    return nnpentity


if __name__ == '__main__':
  app.run()



