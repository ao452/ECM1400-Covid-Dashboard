import schedules as schedules

def test_schedule_covid_updates():
    assert schedules.schedule_covid_updates(update_interval='12:10', update_name='update test')

def schedule_news():
    assert schedules.schedule_news(news_title='update news', news_time ='12:20')

def test_delete_scheduled_update():
    removed_update = schedules.delete_scheduled_update('dwds code4fornews', schedules.schedule_news_update)
    assert not removed_update