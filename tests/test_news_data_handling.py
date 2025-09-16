from covid_news_handling import news_API_request
from covid_news_handling import update_news
import covid_news_handling as cov

#json file for testing purposes
json_for_testing = {
    "status": "ok",
    "totalResults": 18,
    "articles": [
        {
            "source": {
                "id": 'null',
                "name": "Balloon-juice.com"
            },
            "author": "Anne Laurie",
            "title": "COVID-19 Coronavirus Updates: Thursday / Friday, July 21-22",
            "description": "Joe Biden, the oldest person ever to serve as president of the United States, has tested positive for COVID and is experiencing mild symptoms, the White House said https://t.co/RkilR59Z8w pic.twitter.com/dpUSmotXAD \u2014 Reuters (@Reuters) July 21, 2022 DR. PETER\u2026",
            "url": "https://balloon-juice.com/2022/07/22/covid-19-coronavirus-updates-thursday-friday-july-21-22/",
            "urlToImage": "https://balloon-juice.com/wp-content/uploads/2022/07/covid-19-coronavirus-updates-thursday-friday-july-21-22.png",
            "publishedAt": "2022-07-21T11:51:18Z",
            "content": "\u2026 An experimental COVID-19 vaccine in the form of an oral tablet has shown promising immune responses in a small preliminary trial designed mainly to evaluate its safety, according to drug manufactur\u2026 [+1824 chars]"
        },
        {
            "source": {
                "id": 'null',
                "name": "Balloon-juice.com"
            },
            "author": "Anne Laurie",
            "title": "COVID-19 coronavirus updates: Thursday / Friday, July 21-22",
            "description": "Joe Biden, the oldest person ever to serve as president of the United States, has tested positive for COVID and is experiencing mild symptoms, the White House said https://t.co/RkilR59Z8w pic.twitter.com/dpUSmotXAD \u2014 Reuters (@Reuters) July 21, 2022 DR. PETER\u2026",
            "url": "https://balloon-juice.com/2022/07/22/covid-19-coronavirus-updates-thursday-friday-july-21-22/",
            "urlToImage": "https://balloon-juice.com/wp-content/uploads/2022/07/covid-19-coronavirus-updates-thursday-friday-july-21-22.png",
            "publishedAt": "2022-07-22T11:51:18Z",
            "content": "\u2026 An experimental COVID-19 vaccine in the form of an oral tablet has shown promising immune responses in a small preliminary trial designed mainly to evaluate its safety, according to drug manufactur\u2026 [+1824 chars]"
        }]}

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    data = update_news('title')
    assert isinstance(data, list)

def test_sort_news_articles():
    #Above json file is not sorted, after applying sort_news_articles function it is now sorted
    sorted_articles = cov.sort_news_articles(json_for_testing)
    sorted_news_articles = []
    for i in range(len(sorted_articles)):
        sorted_news_articles.append(sorted_articles[i]['publishedAt'])
    assert sorted_news_articles == ['2022-07-22T11:51:18Z', '2022-07-21T11:51:18Z']

def test_remove_duplicate_news_articles():
    #Above json file contains duplicates, this function here is to remove duplicates
    cleaned_articles = cov.remove_duplicate_news_articles(cov.sort_news_articles(json_for_testing))
    #list for storing titles only so we can check if the duplicates were remove
    titles_only = []
    for i in cleaned_articles:
        titles_only.append(i['title'])
    assert len(titles_only) == 1


