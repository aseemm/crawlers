from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

class test():
  def __init__(self):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    self.driver = webdriver.Chrome(options=chrome_options)

  def login_hackernews(self):
    # Get some information about the page
    # print(self.driver.page_source)
    # print(self.driver.title)
    # print(self.driver.current_url)    

    # Search by tag, class, id, xpath, css selector
    # h1 = driver.find_element_by_name('h1')
    # h1 = driver.find_element_by_class_name('someclass')
    # h1 = driver.find_element_by_xpath('//h1')
    # h1 = driver.find_element_by_id('greatID')
    # all_links = driver.find_elements_by_tag_name('a')

    # Accessing elements
    # element.text, elementt.click(), element.get_attribute('class'), element.send_keys('mypassword'), element.is_displayed()
    self.driver.set_window_size(1280, 720)
    self.driver.get("https://news.ycombinator.com/login")
    login = self.driver.find_element_by_xpath("//input").send_keys('hello')
    password = self.driver.find_element_by_xpath("//input[@type='password']").send_keys('world')
    submit = self.driver.find_element_by_xpath("//input[@value='login']").click()

    try:
      logout_button = self.driver.find_element_by_id("logout")
      print('Successfully logged in')
    except NoSuchElementException:
      print('Incorrect login/password')

    # take a screenshot
    self.driver.save_screenshot('screenshot.png')

  def search_google(self):
    self.driver.set_window_size(1280, 720)
    self.driver.get("https://www.google.com/?gws_rd=ssl") 
    self.driver.find_element_by_name("q").click()
    self.driver.find_element_by_name("q").clear()
    self.driver.find_element_by_name("q").send_keys("cat")
    self.driver.find_element_by_id("tsf").submit()
    self.driver.find_element_by_link_text("Images").click() 

  def access_github(self):
    self.driver.set_window_size(1280, 720)
    self.driver.get("https://github.com/TheDancerCodes")
    print(self.driver.title)
    print(self.driver.current_url)
    # print(self.driver.page_source)
    
    # # Wait 20 seconds for page to load
    # timeout = 20
    # try:
    #   WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='avatar width-full rounded-2']")))
    # except TimeoutException:
    #   print("Timed out waiting for page to load")
    #   self.driver.quit()

    # get titles of the pinned repos
    titles_element = self.driver.find_elements_by_xpath("//a[@class='text-bold flex-auto min-width-0 ']")
    titles = [x.text for x in titles_element]
    print('titles:')
    print(titles, '\n')

    language_element = self.driver.find_elements_by_xpath("//p[@class='mb-0 f6 text-gray']")
    languages = [x.text for x in language_element]
    print("languages:")
    print(languages, '\n')

    print("RepoName : Language")
    for title, language in zip(titles, languages):
      print(title + ": " + language)    

automate = test()
# automate.search_google()
# automate.login_hackernews()
automate.access_github()
