# note two things:
# the code can't be run infinitely because the webpage Indeed blocks it after a certain amount of requests
# the URL may be outdated. In this case  please go to indeed.com and fill in the two search-attributes (what, where)
# and copy the URL in the section below. Make sure "...&start" is at the end of the string

# load all the important packages
from pandas.core.frame import DataFrame
import requests

# make sure bs4 is installed as sometimes it is not in the standard version 
from bs4 import BeautifulSoup

# define initial variable to get results function
i = 0
# define lists to fill with values from get result funtion
allJobs = []
allNames = []
allLocations = []

# define how many request (each page is one request) from the indeed side should be made
# note that it is wise to set a low number if you only wants to test the code
maxRequest = 2


def get_results(start=0):
    # define the webpage URL which contains the wanted information. Here it is indeed.com. 
    # If you copy a new URL into the code make sure "....&start" is on the end of the string
    URL = "https://ch.indeed.com/jobs?q=bank&l=Z%C3%BCrich%2C%20ZH&sort=date&vjk=d5485c4c73754612&start=" + str(start)

    # define the webbrowser or in other words the User-Agent to download the HTML structur in the same structure as it is shown
    # on the personal webbrowser. Here, Mozilla Firefox is used
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'}

    # take the URL and make a request. Put in the definded URL and the User-Agent
    page = requests.get(URL, headers=headers)

    # create the soup with the BeautifulSoup Package. 'html.parser' is the most common parser for webscraping.
    # page.text is used to convert the html structure so it can be used in later steps.
    
    soup = BeautifulSoup(page.text, 'html.parser')

    # get variables from outside of the function
    global allJobs, allNames, allLocations
    
    # fill lists with scraped values
    allJobs = allJobs + extract_variables(soup)[0]
    allNames = allNames + extract_variables(soup)[1]
    allLocations = allLocations + extract_variables(soup)[2]


    # stop function after a certain numbers of pages scraped
    global i 
    i = i + 1
    
    # stops the function and gives out the results in three lists
    if i == maxRequest:
        return allJobs, allNames, allLocations 

    # run the code again if there are pages left to scrape
    elif (if_next_page(soup)):
        return get_results(int(start) + 10)

    # return if there are no pages left
    else:
        return allJobs, allNames, allLocations

# function to check whether there are job offers on a page
def if_next_page(soup):
    return True if len(list(soup.find(name='ul', attrs={'class': 'pagination-list'}))) > 5 else False


# function to scrape variables and put them in different lists
def extract_variables(soup):
    # define the lists
    Jobs = []
    Names = []
    Locations = []

    # loop through the soup and find all the wanted tags and extract the text in it
    # all variables can be found under the tag 'div' with the attributes 'class':'job_seen_beacon'
    for item in soup.find_all(name='div', attrs={'class': 'job_seen_beacon'}):
        # get Job description and append in on the list
        Jobs.append(item.find(name='span', attrs={'title': True}).text)

        # get company name and append in on the list
        Names.append(item.find(name='span', attrs={'class': 'companyName'}).text)

        # get job location and append in on the list
        x = str(item.find(name='div', attrs={'class': 'companyLocation'}).text)
        x = x.split('•', 1)
        x = x[0]
        Locations.append(x)

    # return three different list which later can be used
    return Jobs, Names, Locations

# create a dataframe
# get all the variables in different lists
variableLists = get_results()

# define column names for the daraframe
columnNames = ["Job", "CompanyName", "Location"]

# create a dataframe with the help of pandas modul
dfIndeed = DataFrame(variableLists).transpose()
dfIndeed.columns = columnNames

# check the result
print(dfIndeed)