# COVID-19 Data Visualization #

Basic visualization of COVID-19 cases in the state of Pennsylvania. The dataset is web scraped from PA Department of Health COVID-19 Website

## Install Dependencies ##

```
pip install -r requirements.txt
```

* Web Scraping
  * panda
  * beautifulsoup4
  * lxml
* Data Analysis
  * streamlit

## Data Source ##

* Perform Web Scraping to obtain daily data from PA Department of Health:   
      * https://www.health.pa.gov/topics/disease/coronavirus/Pages/Archives.aspx
* Dataset collected:
      * Negative and Positive Cases and Deaths by date
      * Breakdown of numner of cases by county by date
* How to Extract Data
  * Run: python data_extractor_pa.py
  * CSV file produced: **pa_summary.csv**

## Visualization ##

* Jupyter NoteBook - https://github.com/bchan01/covid-19-data-analysis/blob/master/data-analysis.ipynb
  * Dependencies: run data_extractor_pa.py to get up-to-date dataset **pa_summary.csv**
  * jupyter notebook
  * open data-analysis.ipynb
* Streamlit Interactive Visualization App (Coming Soon!!)
