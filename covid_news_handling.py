#IMPORT MODULES
import logging
import requests
import datetime
import os
import json


#Retrieving information about news article from the config file
with open(os.path.join("config/", "config.json"), "r") as config_file:
    config = json.load(config_file)
    newsapi_key = config["News Section Config"]['APIkey']
    news_days = config["News Section Config"]["days"]


def news_API_request(covid_terms = "Covid COVID-19 coronavirus"):
    """
    Api request to newsapi.org to pull the latest news about the Covid
    :param:
        default covid related terms as a String objects
    :return:
        json object with news articles
    """
    recent_dates = str(datetime.datetime.today() - datetime.timedelta(days=5))
    newsdates = recent_dates.split(" ")[0]
    url = ('https://newsapi.org/v2/everything?'
           f'qInTitle={covid_terms}&'
           f'from={newsdates}&'
           'sortBy=popularity&'
           'language=en&'
           f'apiKey={newsapi_key}')
    response = requests.get(url).json()
    news = open(os.path.join("./datasets/", "news.json"), "w", encoding="utf-8")
    news.write(json.dumps(response, sort_keys=False, indent=4))
    logging.info('News data added to JSON')
    return response

def sort_news_articles(newsapi):
    """
    Sorting above file by data published. Most recent ones being on top
    :param:
        json file as an Input
    :return:
        sorted articles by date in descending order
    """
    sorted_articles = sorted(newsapi['articles'], key=lambda d: d['publishedAt'], reverse=True)
    return sorted_articles

def remove_duplicate_news_articles(sorted_articles):
    """
    There were cases of duplicating articles. The function is here to remove those duplicates

    :return:
        List of articles with no duplicates as a json object
    """
    articles = []
    for i in sorted_articles:
        j = i['title'].lower()
        articles.append({'title': j, 'content': i['content']})
    LIST_OF_ARTICLES = []
    temp = []
    for i in range(len(articles)):
        if articles[i]['title'] not in temp:
            LIST_OF_ARTICLES.append({'title': articles[i]['title'].title(), 'content': articles[i]['content']})
            temp.append(articles[i]['title'])
    return LIST_OF_ARTICLES


def update_news(news_title):
    """
    Method for getting up-to-date news regarding Covid
    :returns: ready-to-go news articles
    """
    try:
        news_articles = remove_duplicate_news_articles(sort_news_articles(news_API_request()))
        logging.info("News API Requested")
    except:
        logging.critical("Could not reach the News API ")
    return news_articles

def add_new_article(listofnews, listofdeletednews):
    """
    Adding new news article to the list
    : param:
        list of articles as a json object
        list of deleted news as list
    : return:
        lists of news
        list of deleted news
    """
    for i in sort_news_articles(news_API_request()):
        if i['title'] not in listofnews and i['title'] not in listofdeletednews:
            listofnews.append(i)
            logging.info("COVID API Requested")
            break
    return listofnews, listofdeletednews


