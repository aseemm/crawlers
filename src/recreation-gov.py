from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
import json

class test():
  def __init__(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    self.driver = webdriver.Chrome(options=chrome_options)

  # https://www.recreation.gov/api/search/campsites?start=0&size=1000&fq=asset_id:232447&start_date=2020-07-04T00%3A00%3A00.000Z&end_date=2020-07-07T00%3A00%3A00.000Z&include_unavailable=false


  # https://www.recreation.gov/api/ticket/availability/facility/300015?date=2020-07-14


  # https://www.recreation.gov/api/ticket/availability/facility/300015/monthlyAvailabilitySummaryView?year=2020&month=09&inventoryBucket=FIT
  def yosemite_day_use_tickets(self, year, month):
    url = f'https://www.recreation.gov/api/ticket/availability/facility/300015/monthlyAvailabilitySummaryView?year={year}&month={month}&inventoryBucket=FIT'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()

    for date in resp_json["facility_availability_summary_view_by_local_date"]:
      print(date, resp_json["facility_availability_summary_view_by_local_date"][date]["availability_level"])
      
automate = test()
automate.yosemite_day_use_tickets("2020", "07")
