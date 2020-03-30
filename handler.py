# handler.py
import requests
from bs4 import BeautifulSoup
import datetime
import boto3
import os

def main(event, context):
    # Make a request to get the data
    world_o_meter_url = "https://www.worldometers.info/coronavirus/#countries"
    world_o_s = requests.get(world_o_meter_url).text

    # Script the data via BS
    world_o_soup = BeautifulSoup(world_o_s, "html.parser")
    world_o_countries_table = world_o_soup.find(id='main_table_countries_today')
    world_o_countries_table_rows = world_o_countries_table.find_all('tr')

    # Make a matrix
    WORLD_O_METER_DATA = []
    value_matcher = {
        0: 'country',
        1: 'cases',
        2: 'new_cases',
        3: 'deaths',
        4: 'new_deaths',
        5: 'recovered',
        6: 'active_cases',
        7: 'serious_critical',
        8: 'created_at'
    }
    def convertToInt(val, index):
        if (index) == 0:
            return val.text
        if (index == 8):
            return datetime.datetime.utcnow().date()
        else:
            try:
                int_version = int(val.text.replace(',', ''))
                return int_version
            except ValueError:
                return "<No_Value>"
    for tr in world_o_countries_table_rows[1:]:
        td = tr.find_all('td')
        row = {value_matcher[i]:convertToInt(j, i) for (i,j) in enumerate(td) if i < 9}
        WORLD_O_METER_DATA.append(row)

    # Add the data to dynamoDB table
    client = boto3.client('dynamodb')
    tableName = os.environ['tableName']
    def create_attribute(val):
        str_val = str(val)
        if str_val == '<No_Value>':
            return { 'S': '<No_Value>' }
        return { 'N': str_val }
    try:
        for i in WORLD_O_METER_DATA:
            item = {
                'country': { 'S': i['country'] },
                'cases': create_attribute(i['cases']),
                'new_cases': create_attribute(i['new_cases']),
                'deaths': create_attribute(i['deaths']),
                'new_deaths': create_attribute(i['new_deaths']),
                'recovered': create_attribute(i['recovered']),
                'active_cases': create_attribute(i['active_cases']),
                'serious_critical': create_attribute(i['serious_critical']),
                'created_at': { 'S': i['created_at'] }
            }
            client.put_item(TableName=tableName, Item=item)
        return {
            'statusCode': 200,
            'body': '{"status": "success"}',
        }
    except Exception as exc:
        print(exc)
        return {
            'statusCode': 400,
            'body': '{"status": "fail"}',
        }


if __name__ == "__main__":
    main('', '')