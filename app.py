"""Running the main application"""

#IMPORT MODULES

import datetime
import logging
import logging.config
from flask import Flask, request, render_template

from covid_data_handler import data_runner
from schedules import schedule_covid_updates, updates, schedule_data_update, schedule_news_update, \
    schedule_news, delete_scheduled_update, change_repeat_var
from covid_news_handling import  add_new_article, update_news
from time_calculations import get_time_for_schedules

#initializing flask app
app = Flask(__name__)
app.debug = True

#Configuring logging settings
logging.basicConfig(filename='logs/logs.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')



@app.route('/index/', methods = ['POST', 'GET'])
def index():
    """
        Entry point to run the backend
    """

    #getting the requests for update label box and time box
    update_name = request.args.get("two")
    update_time = str(request.args.get("update")).replace("%3A", ":")
    #if update_label box is checked:
    if update_name:
        #if update covid data is checked
        if request.args.get("covid-data"):
            #then schedule a covid data update
            schedule_covid_updates(update_name,update_time)
            logging.info("Covid data update has been scheduled")
            #if repeat checkbox is checked
            if request.args.get('repeat'):
                for update in updates:
                    if update['content'] == "update covid data":
                        update['repeat'] = True
                        time_till_update = get_time_for_schedules()
                        schedule_data_update.enter(time_till_update + 86400, 1, data_runner, (update_name,))
                        #Once repeating schedule is executed then now update back repeat to False
                        schedule_data_update.enter(time_till_update + 86400, 2, change_repeat_var, (update,))
                logging.info('Repeat for covid data is set')
        #if update news_articles is checked then schedule the news articles update
        if request.args.get("news"):
            #run news scheduling
            schedule_news(update_name,update_time)
            logging.info("News data update has been scheduled")
            #if repeat checkbox is checked
            if request.args.get('repeat'):
                for update in updates:
                    if update['content'] == "update news article":
                        update['repeat'] = True
                        time_till_update = get_time_for_schedules()
                        schedule_news_update.enter(time_till_update+86400, 1, update_news, (update_name,))
                        # Once repeating schedule is executed then now update back repeat to False
                        schedule_news_update.enter(time_till_update+86400, 2, change_repeat_var, (update,))
                logging.info('Repeat for news articles is set')

    #cancelling the scheduled items
    if request.args.get("update_item"):
        #looping through scheduled updates
        for update in updates:
            if request.args.get("update_item") == update['title'] and update['content'] == 'update covid data':
                delete_scheduled_update(request.args.get("update_item"), schedule_data_update)
                logging.info('Scheduled covid update is cancelled')
                #change repeat to False so next line deletes repeat schedule
                update['repeat'] = False
                delete_scheduled_update(request.args.get("update_item"), schedule_data_update)
                updates.remove(update)
            elif request.args.get("update_item") == update['title'] and update['content'] == 'update news article':
                delete_scheduled_update(request.args.get("update_item"), schedule_news_update)
                logging.info('Scheduled news update is cancelled')
                # change repeat to False so next line deletes repeat schedule
                update['repeat'] = False
                delete_scheduled_update(request.args.get("update_item"), schedule_news_update)
                updates.remove(update)
    #removing news articles
    if request.args.get("notif"):
        for article in update_news('News'):
            if request.args.get("notif") == article['title']:
                articles.remove(article)
                deleted_articles.append(article)
                #once the article is removed, new article is added
                add_new_article(articles, deleted_articles)
                logging.info("Following article has been removed " + article['title'])

    #remove scheduled dashboard if it is in a past and repeat is false (repeat already took place or not initilized at all)
    for update in updates:
        currentime = datetime.datetime.now()
        time = currentime.strftime('%H:%M')
        if update['update_time'] <= time and update['repeat'] == False:
            updates.remove(update)

    #running schedulers
    schedule_data_update.run(blocking=False)
    schedule_news_update.run(blocking=False)

    #list of updates in logs
    logging.info("List of updates: %s", updates)
    logging.info("Covid data update scheduler queue: %s", schedule_data_update.queue)
    logging.info("News updates scheduler queue: %s", schedule_news_update.queue)


    ###TODO Fix image
    return render_template('index.html',
                           title = "COVID-19 Dashboard",
                           image='virus_image.png',
                           location = location,
                           nation_location = nation_location,
                           local_7day_infections = local_7day_infections,
                           national_7day_infections = nation_7day_infections,
                           hospital_cases = hospital_cases,
                           deaths_total = deaths_total,
                           updates = updates
                           )

if __name__ == '__main__':
    location, nation_location , local_7day_infections,nation_7day_infections, hospital_cases, deaths_total = data_runner('Covid stats')
    deleted_articles = []
    app.run()