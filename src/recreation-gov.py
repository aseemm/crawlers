from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import requests
import json
from datetime import datetime

recreation_map = {
  'Yosemite Day Use Tickets': '300015',  
  'Yosemite Wawona': '232446',
  'Yosemite Upper Pines': '232447',  
  'Yosemite Tuolumne Meadows': '232448',  
  'Yosemite North Pines': '232449',
  'Yosemite Lower Pines': '232450',    
}

class test():
  def __init__(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    self.driver = webdriver.Chrome(options=chrome_options)

  # Campsite(s)
  # https://www.recreation.gov/api/camps/availability/campground/232447/month?start_date=2020-07-01T00%3A00%3A00.000Z
  def campsites(self, campground_id, year, month):
    url = f'https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month?start_date={year}-{month}-01T00%3A00%3A00.000Z'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()

    print(list(recreation_map.keys())[list(recreation_map.values()).index(campground_id)], month)
    for campsite in resp_json["campsites"]:
      available = [];
      for date in resp_json["campsites"][campsite]["availabilities"]:
        if resp_json["campsites"][campsite]["availabilities"][date] not in ["Reserved", "Not Available", "Not Reservable Management"]:
          date_in_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
          # print(resp_json["campsites"][campsite]["availabilities"][date])
          # save if date is in the future
          if date_in_datetime > datetime.today():
            available.append(date_in_datetime)

      if available:
        print(campsite, end = ' -> '),
        for item in available:
          print(f'{item.month}-{item.day}-{item.year} ({["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][date_in_datetime.weekday()]})', end = ' | ')
        print()
        
  # National Park Ticketed Entry
  # https://www.recreation.gov/ticket/facility/300015 
  # https://www.recreation.gov/api/ticket/availability/facility/300015/monthlyAvailabilitySummaryView?year=2020&month=09&inventoryBucket=FIT
  def day_use_tickets(self, park_id, year, month):
    url = f'https://www.recreation.gov/api/ticket/availability/facility/300015/monthlyAvailabilitySummaryView?year={year}&month={month}&inventoryBucket=FIT'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    resp_json = resp.json()

    available = [];
    for date in resp_json["facility_availability_summary_view_by_local_date"]:
      if resp_json["facility_availability_summary_view_by_local_date"][date]["availability_level"] == "LOW":
        date_in_datetime = datetime.strptime(date, "%Y-%m-%d")
        # save if date is in the future
        if date_in_datetime > datetime.today():        
          available.append(date_in_datetime)        

    print(list(recreation_map.keys())[list(recreation_map.values()).index(park_id)], month)
    if available:
      for item in available:
        print(f'{item.month}-{item.day}-{item.year} ({["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][date_in_datetime.weekday()]})', end = ' | ')
      print()
      
automate = test()
automate.day_use_tickets(recreation_map["Yosemite Day Use Tickets"], "2020", "06")
automate.day_use_tickets(recreation_map["Yosemite Day Use Tickets"], "2020", "07")
automate.day_use_tickets(recreation_map["Yosemite Day Use Tickets"], "2020", "08")

automate.campsites(recreation_map["Yosemite Upper Pines"], "2020", "06")
automate.campsites(recreation_map["Yosemite Upper Pines"], "2020", "07")
automate.campsites(recreation_map["Yosemite Upper Pines"], "2020", "08") 

automate.campsites(recreation_map["Yosemite Wawona"], "2020", "07")
automate.campsites(recreation_map["Yosemite North Pines"], "2020", "07")
automate.campsites(recreation_map["Yosemite Lower Pines"], "2020", "07")
automate.campsites(recreation_map["Yosemite Tuolumne Meadows"], "2020", "07") 
