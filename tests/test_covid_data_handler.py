import covid_data_handler as cov
from covid_data_handler import process_covid_csv_data
import pandas as pd


def test_parse_csv_data():
    data = cov.parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( cov.parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = cov.covid_API_request()
    assert isinstance(data, dict)

def test_covid_local_api_request():
    data = cov.covid_local_api_request()
    assert isinstance(data, pd.DataFrame)

def test_covid_nation_api_request():
    data = cov.covid_nation_api_request()
    assert isinstance(data, pd.DataFrame)




