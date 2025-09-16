
# IMPORT MODULES
import logging
import sched
import time

from covid_data_handler import data_runner
from covid_news_handling import update_news
from time_calculations import get_time_for_schedules


#FUNCTIONS FOR SCHEDULING UPDATES

#initialized empty list to store all the scheduled updates
updates = []


schedule_data_update = sched.scheduler(time.time, time.sleep)
def schedule_covid_updates(update_name, update_interval):
    """
    Method for scheduling covid updates
    :param update_name: name of the update
    :param update_interval: interval at which update will take place
    """
    time_till_update = get_time_for_schedules()
    data_title = update_name
    data_time = update_interval
    updates.append({"title": data_title + ' code4forcovid',
             "update_time": data_time,
             "update_interval": time_till_update,
             "repeat": False,
             "content": "update covid data"})
    schedule_data_update.enter(time_till_update, 1, data_runner, (update_name,))



schedule_news_update = sched.scheduler(time.time, time.sleep)
def schedule_news(news_title, news_time):
    """
    Method for scheduling covid updates
    :param update_name: name of the update
    :param update_interval: interval at which update will take place
    """
    time_till_update = get_time_for_schedules()
    updates.append({"title":news_title + ' code4fornews',
                    "update_time": news_time,
                    "update_interval": time_till_update,
                    "repeat": False,
                    "content": "update news article"})
    schedule_news_update.enter(time_till_update, 1, update_news, (news_title,))


def delete_scheduled_update(update_name, scheduler):
    """
    Method for deleting scheduled update if cancel button is pressed
    :param update_name: title of the cancelling update
    :param scheduler: one of the two scheduler (schedule_data_update, schedule_news_updatE)
    """
    #list of words for separating covid update from news update
    #code4forcovid = covid update
    #code4fornews = news article update
    stopwords = ['code4forcovid', 'code4fornews']
    for i in stopwords:
        update_name = update_name.replace(i, '')
    string_to_tuple = " ".join(update_name.split()),
    #looping through scheduler and seeing if update_name equals to item in scheduler
    #if yes then cancel it
    for i in scheduler.queue:
        if string_to_tuple == i.argument:
            scheduler.cancel(i)
            logging.info('Scheduled data is deleted')
            break


def change_repeat_var(update_item):
    """
    Method for updating repeat to false so there will be no repeat after it took place once

    :param update_item: update dictionary value of which is updating
    """
    update_item['repeat'] = False



