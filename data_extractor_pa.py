import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import os
from datetime import datetime

SUMMARY_FILE = 'pa_summary.csv'
COUNTY_FILE = 'pa_county.csv'

CUTOFF_DATE = 'March 17, 2020'

def extract_dates(soup):
    # Extract Date Headers
    # Web Site contains completed data dating back to March 18
    cutoff_date = parse(CUTOFF_DATE)
    date_headings = []
    for heading in soup.find_all('h4'):
        heading_value = heading.text.strip()
        if heading_value.startswith('March') or heading_value.startswith('April'):
            dt = parse(heading.text)
            if dt > cutoff_date:
                print('H4: %s' % heading_value)
                date_headings.append(dt.strftime('%Y-%m-%d'))
    print('Date Count: %d' % len(date_headings))
    return date_headings


def extract_summary_data(soup, date_list):

    table_body_sections = soup.find_all('tbody')
    dataset_columns = ['Date', 'Negative', 'Positive', 'Deaths']
    data_rows = []
    data_rows.append(','.join(dataset_columns))
    count = 0
    for table_body in table_body_sections:
        rows = table_body.find_all('tr')
        if len(rows) != 2:
            continue
        header_row = rows[0]
        # Filter out other tables
        if len(header_row) < 2 or len(header_row) > 3:
            continue
        columns = header_row.find_all('td')
        columns = [x.text.strip().replace('\u200b', '') for x in columns]
        
        if columns[0] == 'Negative':
            data_row = rows[1]
            columns = data_row.find_all('td')
            columns = [x.text.strip().replace('\u200b', '').replace(',', '') for x in columns]
            columns.insert(0, date_list[count])
            if len(columns) == 3:
                columns.append('0')
            print(columns)
            data_rows.append(','.join(columns))
            count += 1

            if count > len(date_list) :
                print('End of Date to process - EXIT')
                break

    print('Total Summary Rows Extracted: %d' % count)
    if os.path.exists(SUMMARY_FILE):
            os.remove(SUMMARY_FILE)
    
    line = 0
    with open(SUMMARY_FILE, 'w') as file:
        for row in data_rows:
            if line > 0:
                file.write('\n')
            file.write(row)
            line += 1

def extract_county_data(soup, date_list):
    
    table_body_sections = soup.find_all('tbody')
    dataset_columns = ['Date', 'County', 'Cases', 'Deaths']
    data_rows = []
    data_rows.append(','.join(dataset_columns))
    count = 0
    for table_body in table_body_sections:
        rows = table_body.find_all('tr')
        header_row = rows[0]

        # Header can be td or th
        columns = header_row.find_all('th')
        if columns is None or len(columns) < 1:
            columns = header_row.find_all('td')
        columns = [x.text.strip().replace('\u200b', '') for x in columns]
        if len(columns) < 1:
            continue;
        
        startIdx = -1
        # County, Number of Cases|Cases, Deaths
        if columns[0] == 'County':
            startIdx = 1
        # Special Case: March 19, 2020 - no header
        elif columns[0] == 'Adams':
            startIdx = 0

        if startIdx == -1:
            continue

        # Collect County Rows
        for i in range(startIdx, len(rows)):
            data_row = rows[i]
            columns = data_row.find_all('td')
            columns = [x.text.strip().replace('\u200b', '').replace(',', '') for x in columns]
            columns.insert(0, date_list[count])
            if len(columns) == 3:
                columns.append('0')
            elif columns[3] == '':
                columns[3] = '0'
            #print(columns)
            data_rows.append(','.join(columns))
        print('Total County Rows Extracted: %d for date: %s' % (len(rows), date_list[count]))
        count += 1
        if count > len(date_list):
            print('End of Date to process - EXIT')
            break

    print('Total County Sections Extracted: %d' % count)
    if os.path.exists(COUNTY_FILE):
            os.remove(COUNTY_FILE)
    
    line = 0
    with open(COUNTY_FILE, 'w') as file:
        for row in data_rows:
            if line > 0:
                file.write('\n')
            file.write(row)
            line += 1

def main() :
    res = requests.get('https://www.health.pa.gov/topics/disease/coronavirus/Pages/Archives.aspx')
    soup = BeautifulSoup(res.content, 'lxml')
    date_list = extract_dates(soup)
    extract_summary_data(soup, date_list)
    extract_county_data(soup, date_list)


if __name__ == "__main__":
    # execute only if run as a script
    main()
