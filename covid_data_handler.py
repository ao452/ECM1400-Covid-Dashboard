#IMPORT MODULES
import csv
import pandas as pd
import os
import json
import logging

from uk_covid19 import Cov19API




def parse_csv_data(csv_filename = 'nation_2021-10-28.csv'):
    """
    Reads csv data that was given as a sample dataset

    :returns:
        csv file with sample covid dataset
    """
    with open(csv_filename, newline = '') as f:
        reader = csv.reader(f)
        csv_list = list(reader)
    return csv_list




def process_covid_csv_data(covid_csv_data):
    """
    Processes covid_csv file above
    : param:
        Pandas DataFrame as Input
    : returns:
        The number of cases in the past 7 days,
        The number of hospital cases
        The number of cumulative deaths
    """
    total_cases_for_last_7days = 0
    day_counter = 0
    for i in covid_csv_data[3:]:
        print(i)
        total_cases_for_last_7days += int(i[6])
        day_counter += 1
        if day_counter == 7:
            break

    current_hospital_cases = 0
    day_counter = 0
    for i in covid_csv_data[1:]:
        current_hospital_cases = i[5]
        day_counter += 1
        if day_counter == 1:
            break

    cumulitive_death = 0
    day_counter = 0
    for i in covid_csv_data[2:]:
        if i[4] != "":
            cumulitive_death = i[4]
            day_counter += 1
            if day_counter == 1:
                break



    return total_cases_for_last_7days, int(current_hospital_cases), int(cumulitive_death)

def covid_API_request():
    """"
        Api request to the Cov19Api and getting the local covid data
        : return:
            Covid data as a json file
        """
    covid_api = Cov19API(filters=covapi_filters_local, structure=covapi_structure)
    covid_api = covid_api.get_json()
    return covid_api


#TODO rewrite config file type
with open(os.path.join("config/", "config.json"), "r") as config_file:
    config = json.load(config_file)
    covapi_filters_local = config["Covid Data Config"]['Local Data']
    covapi_filters_nation = config["Covid Data Config"]['Nation Data']
    covapi_structure= config["Covid Data Config"]["Output Format"]


def covid_local_api_request():
    """"
    Api request to the Cov19Api and getting the local covid data
    : return:
        Covid data as a Pandas dataframe (csv file)
    """

    covid_api = Cov19API(filters=covapi_filters_local, structure=covapi_structure)
    covapi_csv = covid_api.get_dataframe()
    covapi_csv.to_csv('datasets/covapi_data.csv')
    logging.info('COVID local data added to CSV file')
    return covapi_csv

def covid_nation_api_request():
    """"
    Api request to the Cov19Api and getting the national covid data
    : return:
        Covid data as a Pandas dataframe (csv file)
    """

    covid_api_nation = Cov19API(filters=covapi_filters_nation, structure=covapi_structure)
    covapi_nation_csv = covid_api_nation.get_dataframe()
    covapi_nation_csv.to_csv('datasets/covapi_nation_data.csv')
    logging.info('COVID nation data added to CSV file')
    return covapi_nation_csv



def process_covid_realdata(covid_ltle_csv_data, covid_nation_csv_data):
    """
    Process the covid data obtained above
    : param:
        Pandas dataframe with covid information as an input
    : return:
        number of cases for the last 7 days (local)
        number of cases for the last 7 days (national)
        last recorded number of hospital cases
        last recorded number of deaths
    """
    #stats of region
    df_ltle = pd.DataFrame(covid_ltle_csv_data)
    df_ltle = df_ltle.fillna(0)
    location_ltle = df_ltle['areaName'][0]
    cases_ltle_7day = df_ltle['newCasesByPublishDate'].head(7).sum()

    #stats of nation
    df_nation = pd.DataFrame(covid_nation_csv_data)
    df_nation = df_nation.fillna(0)
    location_nation = df_nation['areaName'][0]
    cases_nation_7day = df_nation['newCasesByPublishDate'].head(7).sum()

    #get stats for hospital cases
    try:
        if df_nation.hospitalCases.values.sum() < 0:
            hospital_cases = 0
        else:
            hospital_cases = df_nation.hospitalCases.loc[df_nation.hospitalCases != 0].iloc[0]
    except IndexError:
        hospital_cases = 0

    #get stats for deaths
    if df_nation.cumDeaths28DaysByDeathDate.values.sum() < 0:
        death_cases = 0
    else:
        death_cases = df_nation.cumDeaths28DaysByDeathDate.loc[df_nation.cumDeaths28DaysByDeathDate != 0].iloc[0]

    return location_ltle, location_nation, int(cases_ltle_7day), int(cases_nation_7day), int(hospital_cases), int(death_cases)


#get update-to-date covid stats
def data_runner(update_name):
    """
    Method for getting ready-to-go covid data
    :returns: all the required statistics
    """
    try:
        location_ltle, location_nation, cases_ltle_7day, cases_nation_7day, hospital_cases, death_cases = process_covid_realdata(covid_local_api_request(), covid_nation_api_request())
        logging.info("COVID API Requested")
    except:
        logging.critical("Could not reach the COVID API ")
    return location_ltle, location_nation,cases_ltle_7day,cases_nation_7day, hospital_cases, death_cases

