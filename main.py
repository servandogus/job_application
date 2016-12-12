# -*- coding: utf-8 -*-

import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import html



def get_session(url, params):
    session = requests.session()
    res = session.get(url, data = params)
    return res
    
def get_EFC_results(keywords,locationsId="3017382"):
    ''' return a DataFrame :
    JobTitle | Link | Salary | Location | PositionType | Comptany | Date | Summary | Description '''
    
    url_web = "http://www.efinancialcareers.com/search"    
    params = { "keywords" : keywords,
              "sortBy" : "POSTED_DESC",
              "locationsId[0]" : locationsId
    }
    
    page = requests.get(url_web, params = params)
    tree = html.fromstring(page.text)
    
    JobTitle = tree.xpath('//li[@class="jobPreview well"]/h3/a/text()')
    Link = tree.xpath('//li[@class="jobPreview well"]/h3/a/@href')
    Salary = tree.xpath('//li[@class="jobPreview well"]/ul[@class="details"]/li[@class="salary"]/span/text()')
    Location = tree.xpath('//li[@class="jobPreview well"]/ul[@class="details"]/li[@class="location"]/span/text()')
    PositionType = tree.xpath('//li[@class="jobPreview well"]/ul[@class="details"]/li[@class="position"]/span/span/text()')
    Company = tree.xpath('//li[@class="jobPreview well"]/ul[@class="details"]/li[@class="company"]/span/text()')
    Date = tree.xpath('//li[@class="jobPreview well"]/ul[@class="details"]/li[@class="updated"]/span/text()')
    
    JobTitle = list( map(lambda x : str(x), JobTitle))
    Link = list(map(lambda x : str(x), Link))
    Salary = list(map(lambda x : str(x), Salary))
    Location = list(map(lambda x : str(x), Location))
    PositionType = list(map(lambda x : str(x), PositionType))
    Company = [str(x).split(" ")[-1] for x in Company]
    Date = [str(x).split("\xa0")[-1] for x in Date]
    Summary = [get_EFC_summary(u) for u in Link]
    Description = [get_EFC_description(u) for u in Link]
    
    DF = pd.DataFrame({'JobTitle':JobTitle, 'Link':Link,'Salary':Salary,'Location':Location,'PositionType':PositionType,'Company':Company,'Date':Date,'Summary':Summary,'Description':Description})    
    
    return DF

def get_EFC_description(url_job):
    ''' For a job url, return the description in a string'''
    try:
        page = requests.get(url_job)
        soup = BeautifulSoup(page.text,'lxml')
        
        description = soup.find("section",class_="description").find("div",class_="well").find("div",class_="body").text
    except:
        description = soup.find("section",class_="description").text
    return description

def get_EFC_summary(url_job):
    ''' For a job url, return the summary in a string'''
    try:
        page = requests.get(url_job)
        soup = BeautifulSoup(page.text,'lxml')
        
        summary = soup.find("section",class_="description").find("div",class_="well").find("p",class_="summary").text
    except:
        return ''
    return summary

# utilisation
d = get_EFC_results("python")
    