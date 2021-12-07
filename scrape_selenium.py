from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
driver = webdriver.Chrome("./chromedriver")
driver.fullscreen_window()
try:
    df = pd.read_csv('php_developer_jobs.csv', sep='|')
except:
    df = pd.DataFrame(columns=["Title", "Description"])

for i in range(0, 250, 50):
    driver.get('https://www.indeed.com/jobs?q=title%3A%28"wordpress+web+developer"+or+"wordpress+developer"+or+'
               '"wordpress+webmaster"+or+"wordpress+engineer"+or+"wordpress+website+developer"+or+'
               '"wordpress+frontend+developer"+or+"wordpress+front+end+developer"+or+"lamp+developer"+or+'
               '"lamp+stack+developer"+or+"lamp+fullstack+developer"+or+"lamp+full+stack+developer"+or+'
               '"lamp+stack+engineer"+or+"lamp+web+developer"+or+"lamp+engineer"+or+"lamp+software+engineer"+or+'
               '"magento+developer"%29&limit=50&start=' + str(i))
    jobs = []
    driver.implicitly_wait(5)
    for job in driver.find_elements_by_class_name("result"):
        soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
        try:
            event = soup.find("table", class_="jobCardShelfContainer")
        except:
            event = None
        if event is not None:
            continue
        try:
            title = soup.find("a", class_="jobtitle").text.replace("\n", "").strip()
        except:
            title = 'None'
        sum_div = job.find_element_by_xpath('./div[3]')
        try:
            sum_div.click()
        except:
            close_button = driver.find_elements_by_class_name('popover-x-button-close')[0]
            close_button.click()
            sum_div.click()
        try:
            job_desc = driver.find_element_by_id('vjs-desc').text
        except:
            try:
                close_button = driver.find_elements_by_class_name('popover-x-button-close')[0]
                close_button.click()
                sum_div.click()
            except:
                sum_div.click()
            job_desc = driver.find_element_by_id('vjs-desc').text
        df = df.append({'Title': title, "Description": job_desc}, ignore_index=True)
        print("Got these many results:", df.shape)
pd.DataFrame(df.Title.value_counts()).to_csv("php_dev_unique_title_counts.csv")
df.to_csv("php_developer_jobs.csv", index=False, sep='|')
