import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import os

SUMMARY_FILE = 'pa_summary.csv'

def extract_dates(soup):
    # Extract Date Headers
    # Web Site contains completed data dating back to March 18
    cutoff_date = parse('March 17, 2020')
    date_headings = []
    for heading in soup.find_all('h4'):
        heading_value = heading.text.strip()
        if heading_value.startswith('March') or heading_value.startswith('April'):
            dt = parse(heading.text)
            if dt > cutoff_date:
                print('H4: %s' % heading_value)
                date_headings.append(dt)
    print('Date Count: %d' % len(date_headings))
    return date_headings

def extract_summary_row(soup, date_list):
    df_summary = None
    data_row_count = 0
    for table in soup.find_all('table'):
        df = pd.read_html(str(table), header=0)[0]
        columns = list(df.columns)
        if len(columns) >= 2 and columns[0] == '​Negative' and columns[1] == 'Positive':
            df.insert(loc=0, column='Date', value= date_list[data_row_count])
            print(df)
            if df_summary is None:
                df_summary = df
            else:
                df_summary = pd.concat(
                    [df_summary, df], sort=False, ignore_index=True)
            data_row_count += 1

    print('Merged Data Row Count: %d' % len(df_summary))

    df_summary = df_summary.fillna(0)
    print(df_summary)

    if os.path.exists(SUMMARY_FILE):
        os.remove(SUMMARY_FILE)
    df_summary.to_csv(SUMMARY_FILE, index=False, header=True)

def main() :
    res = requests.get('https://www.health.pa.gov/topics/disease/coronavirus/Pages/Archives.aspx')
    soup = BeautifulSoup(res.content, 'lxml')
    date_list = extract_dates(soup)
    extract_summary_row(soup, date_list)


if __name__ == "__main__":
    # execute only if run as a script
    main()
