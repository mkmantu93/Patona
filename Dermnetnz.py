######### Mantu Kumar ####### 08/11/2022

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import zipfile
import re
from datetime import datetime
from bs4 import BeautifulSoup
import os
from random import randint
from time import sleep
import pandas as pd
import csv

class Dermnetnz:

    def __init__(self):
        self.domain = 'https://dermnetnz.org'
        self.proxy = None
        self.retries=None
        self.current_path = os.path.dirname(os.path.abspath(__file__)) + '/'

    def Initiate(self):
        try:
            self.push_data_to_file(','.join(["Name of Diseases","URLs","Icon images of diseases"]) + '\n')
            # with open(self.current_path + "Input.txt", "r", encoding='utf-8') as f:
            #     self.inputs = f.readlines()
            self.inputs = ['https://dermnetnz.org/image-library']
        except Exception as e:
            print('Bad supporting files ---------exiting without crawling\n Error => ' + str(e))
            quit()

        for data in self.inputs:
            try:
                if data[0] != "#":
                    line = data.split("\t")
                    self.lines=line
                    Url=line[0].strip()
                    if Url != "":
                        self.input_url = Url.rstrip()
                        self.Hitting_url(self.input_url, False)
            except Exception as e:
                print(e, "Error code 000---")
                self.push_data_to_log('\t'.join(self.lines) + "\t" + str(e) + "\n")

    def Hitting_url(self, url, Main):

        while True:
            try:
                chrome_options = webdriver.ChromeOptions()
                self.driver = webdriver.Chrome( chrome_options=chrome_options)
                self.driver.get(url)
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dermnetz2_incontent_images_and_glossary"]')))
                sleep(randint(1,5))
                self.fetch_data(url)
                return
            except Exception as e:
                self.Close_driver()
                self.retries += 1
                if self.retries < 2:
                    print('Bad Response - Retrying:', self.retries)
                    print('error cause -', str(e), '\n')
                    continue
                else:
                    print(
                        "---Failed to Connect after max retries--- \n Error -> {} :----: Exiting with code 001".format(
                            e))
                    self.push_data_to_log('\t'.join(self.lines) + "\t" + str(e) + "\n")
                    return None

    def Close_driver(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception as e:
            pass

    def remove_junk(self, text):
        text = re.sub(r'\r+|\n+|\t+|\s+', ' ', text)
        return text.strip()

    def fetch_data(self, url):
        try:
            try:

                parser = html.document_fromstring(self.driver.page_source)
                all_diseases_urls=parser.xpath('//*[@class="imageList__group"]/div//a/@href')
                all_diseases_names=parser.xpath('//*[@class="imageList__group"]/div//a/div[2]/h6/text()')
                all_diseases_imgs = parser.xpath('//*[@class="imageList__group"]/div//a/div[1]/img/@src')
                for all_diseases_name,all_diseases_url,all_diseases_img in zip(all_diseases_names,all_diseases_urls,all_diseases_imgs):
                    Record = []
                    all_diseases_name=''.join(self.remove_junk(all_diseases_name))
                    Record.append(all_diseases_name)
                    all_diseases_url=''.join(self.remove_junk(all_diseases_url))
                    all_diseases_url=str(self.domain+all_diseases_url).strip()
                    Record.append(all_diseases_url)
                    all_diseases_img=''.join(self.remove_junk(all_diseases_img))
                    Record.append(all_diseases_img)
                    record = list(map(str, Record))
                    record = list(map(lambda x: x.replace('\n', ' ').replace('None', ''), record))

                    self.push_data_to_file(','.join(record) + '\n')

                print('---- Data Inserted ---')
                return
            except Exception as e:
                print("Error in parser" + str(e))
        except Exception as e:
            print('---- Parsing error ---', e)
            self.push_data_to_log('\t'.join(self.lines) + "\t" + str(e) + "\n")

    def push_data_to_file(self, data):
        with open(self.current_path + "dermnetnz_output_data.csv", "a") as f:
            f.write(data)
    def push_data_to_log(self, data):
        with open(self.current_path + "log.txt", "a", encoding='utf-8') as f:
            f.write(data)

if __name__ == "__main__":
    a = Dermnetnz()
    a.Initiate()
