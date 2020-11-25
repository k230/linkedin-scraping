from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
import parameters
import  csv
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import requests
import json
import  pickle
import pandas as pd

driver = webdriver.Firefox(executable_path="C://Users//C_v//PycharmProjects//New folder//geckodriver.exe")

driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys(parameters.linkedin_username)


password = driver.find_element_by_id('session_password')

password.send_keys(parameters.linkedin_password)

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()

driver.get('https://www.linkedin.com/search/results/people/?keywords=cloud&origin=SWITCH_SEARCH_VERTICAL')



src = driver.page_source
soup = BeautifulSoup(src, 'lxml')
data=[]
for i in soup.find_all('code'):
    try :
        data.append(json.loads(i.text))
    except:
        pass

# for i in range(2,1000):
#     i=str(i)
#     sleep(2)
#     driver.get('https://www.linkedin.com/search/results/people/?keywords=cloud&origin=SWITCH_SEARCH_VERTICAL&page='+i)
#
#     src_link = driver.page_source
#     soup_link = BeautifulSoup(src_link, 'lxml')
#     for j in soup_link.find_all('code'):
#         try :
#             data.append(json.loads(j.text))
#         except:
#             pass
#



links=[]
for i in data:

    if 'data' in i.keys():
         try:
             for j in i['data']['elements']:
                 if "extendedElements" in j.keys():
                     for k in j['elements']:
                         links.append(k['navigationUrl'])

         except:
             pass
list_dict_profiles=[]
k=0
for i in links:
    dict_profiles = {}
    if k<1:
        k=k+1
        driver.get(i)
        sleep(15)
        pro_src = driver.page_source
        pro_soup = BeautifulSoup(pro_src, 'lxml')
        for name_vib in pro_soup.find_all('li',{'class':'inline t-24 t-black t-normal break-words'}):
            dict_profiles['Name']=name_vib.text
        for summary_vib in pro_soup.find_all('h2',{'class':'mt1 t-18 t-black t-normal break-words'}):
            dict_profiles['Summary']=summary_vib.text
        for location_vib in pro_soup.find_all('li',{'class':'t-16 t-black t-normal inline-block'}):
            dict_profiles['Location']=location_vib.text
        for education_vib_name in pro_soup.find_all('h3',{'class':'pv-entity__school-name t-16 t-black t-bold'}):
            dict_profiles['Institute']=education_vib_name.text
        for education_vib_digree in pro_soup.find_all('span',{'class':'pv-entity__comma-item'}):
            dict_profiles['Digree']=education_vib_digree.text
        for post_vib in pro_soup.find_all('h3',{'class':'-t-16 t-black t-bold'}):
            dict_profiles['Post']=post_vib.text
        for company_vib in pro_soup.find_all('p',{'class':'pv-entity__secondary-title t-14 t-black t-normal'}):
            dict_profiles['Company']=company_vib.text
        for experience_vib in pro_soup.find_all('span',{'class':'pv-entity__bullet-item-v2'}):
            dict_profiles['Experience']=experience_vib.text
        for  skills_endorsements_vib in pro_soup.find_all('section',{'class':'pv-profile-section pv-skill-categories-section artdeco-container-card artdeco-card ember-view'}):
            dict_profiles['Skills & endorsements']=skills_endorsements_vib.text
        for  recommendations_vib in pro_soup.find_all('div',{'class':'recommendations-inlining'}):
            dict_profiles['Recommendations']=recommendations_vib.text
        for  accomplishments_vib in pro_soup.find_all('section',{'class':'pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view'}):
            dict_profiles['Accomplishments']=accomplishments_vib.text
        try:
            driver.get(i+'/detail/interests/influencers/')
            sleep(2)
            influencers_src = driver.page_source
            influencers_soup = BeautifulSoup(influencers_src, 'lxml')
            for influencers_name in influencers_soup.find_all('span',{'class':'pv-entity__summary-title-text'}):
                dict_profiles['interst_Influencer_Name']=influencers_name.text
            for influencers_des in influencers_soup.find_all('p',{'class':'pv-entity__occupation t-14 t-black--light t-normal'}):
                dict_profiles['interst_Influencer_des']=influencers_des.text
            for influencers_foll in influencers_soup.find_all('p',{'class':'pv-entity__follower-count t-14 t-black--light t-normal'}):
                dict_profiles['interst_Influencer_foll']=influencers_foll.text
        except:
            pass
        try:
            driver.get(i+'/detail/interests/companies/')
            sleep(15)
            companies_src = driver.page_source
            companies_soup = BeautifulSoup(companies_src, 'lxml')
            for companies_name in companies_soup.find_all('ul',{'class':'entity-list row'}):
                dict_profiles['interst_Company']=companies_name.text
        except:
            pass
        try:
            driver.get(i+'/detail/interests/groups/')
            sleep(15)
            groups_src = driver.page_source
            groups_soup = BeautifulSoup(groups_src, 'lxml')
            for groups in groups_soup.find_all('ul',{'class':'entity-list row'}):
                dict_profiles['interst_group']=groups.text
        except:
            pass
        try:

            driver.get(i+'/detail/interests/schools/')
            sleep(15)
            schools_src = driver.page_source
            schools_soup = BeautifulSoup(schools_src, 'lxml')
            for schools in schools_soup.find_all('ul',{'class':'entity-list row'}):
                dict_profiles['interst_school']=schools.text
        except:
            pass

        try:
            driver.get(i+'/detail/contact-info/')
            sleep(2)
            contact_info_src = driver.page_source
            contact_info_soup = BeautifulSoup(contact_info_src, 'lxml')
            for contact_info_vib in contact_info_soup.find_all('a',{'class':'pv-contact-info__contact-link link-without-visited-state t-14'}):
                dict_profiles['Contact_info']=contact_info_vib.text
        except:
            pass
        list_dict_profiles.append(dict_profiles)


print(list_dict_profiles)
df=pd.DataFrame(list_dict_profiles)
print(df)
df.to_csv('Data.csv',index=False)
