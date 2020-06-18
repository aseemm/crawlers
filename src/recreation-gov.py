from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
import json
from datetime import datetime

class test():
  def __init__(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    self.driver = webdriver.Chrome(options=chrome_options)

  # Yosemite Campsite(s)
  # https://www.recreation.gov/api/camps/availability/campground/232447/month?start_date=2020-07-01T00%3A00%3A00.000Z
  def yosemite_campsites(self, campground_id, year, month):
    url = f'https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month?start_date={year}-{month}-01T00%3A00%3A00.000Z'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()
    for campsite in resp_json["campsites"]:
      available = [];
      for date in resp_json["campsites"][campsite]["availabilities"]:
        if resp_json["campsites"][campsite]["availabilities"][date] not in ["Reserved", "Not Available"]:
          date_in_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
          available.append(date_in_datetime)
      if available:
        print(campsite, end = ' -> '),
        for item in available:
          print(f'{item.month}-{item.day}-{item.year} ({["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][date_in_datetime.weekday()]})', end = ' | ')
        print()
        
  # Yosemite National Park Ticketed Entry
  # https://www.recreation.gov/ticket/facility/300015 
  # https://www.recreation.gov/api/ticket/availability/facility/300015/monthlyAvailabilitySummaryView?year=2020&month=09&inventoryBucket=FIT
  def yosemite_day_use_tickets(self, year, month):
    url = f'https://www.recreation.gov/api/ticket/availability/facility/300015/monthlyAvailabilitySummaryView?year={year}&month={month}&inventoryBucket=FIT'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()

    for date in resp_json["facility_availability_summary_view_by_local_date"]:
      if resp_json["facility_availability_summary_view_by_local_date"][date]["availability_level"] == "LOW":
        date_in_datetime = datetime.strptime(date, "%Y-%m-%d")
        print(date, "(", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][date_in_datetime.weekday()], ")", resp_json["facility_availability_summary_view_by_local_date"][date]["availability_level"])
      
automate = test()
# automate.yosemite_day_use_tickets("2020", "07")
automate.yosemite_campsites("232447", "2020", "07") # upper pines
