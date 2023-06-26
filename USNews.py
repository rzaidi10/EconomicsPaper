import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib



# Define the URL of the website to scrape

# data is a set of dictionaries of each college with all the info
data = []

# header is used to bypass error blockers (too many requests, etc.)
# might need to find your own computer's user agent
header = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15,",
    
    'referer':'https://www.niche.com/'
    }

# 109 niche pages
for i in range (1,109):
    # using cached form to avoid getting rejected
	nicheURL = 'http://webcache.googleusercontent.com/search?q=cache:https://www.niche.com/colleges/search/best-colleges/?page='+str(i)
    nichePage = requests.get(nicheURL)
    soup = BeautifulSoup(nichePage.content,"html.parser")
    print("PAGE",i,":",nicheURL)

    #with open("/Users/arinjaff/Downloads/niche.html", 'rb') as fp:
    # soup = BeautifulSoup(fp)

        # Find all the links to college pages
    college_links = soup.find_all("a", class_="search-result__link")


    # popping ads out
    college_links.pop(3)
    college_links.pop(25)
    college_links.pop(25)

    # getting links
    college_urls = []
    for link in college_links:
        href = link.get("href")
        if href and re.search(r"/colleges/\S+", href):
            if not link.find("h2", string="Sponsored Result"):
                college_urls.append(href)
            else:
                print("excluded" + href)
    #print("URLS:",college_urls)
    for college_url in college_urls:
        
        print(college_url)

        # using cache to avoid getting rejected from website
        newUrl = "http://webcache.googleusercontent.com/search?q=cache:"+college_url
        college_response = requests.get(newUrl,headers=header)

        #print(college_response)
        
        college_response = requests.get(newUrl)
        college_soup = BeautifulSoup(college_response.content, "html.parser")
        #print(college_response.content)

        #print(college_response.content)
		
		# getting college info
        college = college_soup.find("div", class_="postcard__content postcard__content--primary").text.strip()

		# getting college name (depending on format)
        college_name = college.split("#")[0].strip()
        college_name = college.split("This")[0].strip()

        # Extract college rank
        college_rank = college_urls.index(college_url)+1

        # Extract state
        state_match = re.search(r",\s*([A-Z]{2})", college)
        state = state_match.group(1) if state_match else None

        gradeTable = []
        i = 0
        trueCheck = True
        while trueCheck:
            #print("hi")
            try:
                gradeTable.append(college_soup.findAll("li",class_="ordered__list__bucket__item")[i].text.strip())
                i = i+1
            except:
                trueCheck = False
        grades_dict = {}
        for item in gradeTable:
            category, grade = item.split("grade\xa0")

            grade = grade.replace(" minus", "-")  # Replace "minus" with "-"
            grades_dict[category] = grade
                            
    #print(grades_dict)
        try:
            desc = college_soup.find("span",class_="bare-value").text.strip()
                #  number of students
            students_match = re.search(r"(\d{1,3}(?:,\d{3})*)(?: undergraduate)? students", desc)
            if students_match:
                number_of_students = students_match.group(1).replace(",", "")
            else:
                number_of_students = None

            # popular majors
            majors_match = re.search(r"majors include (.+?)\.", desc)
            if majors_match:
                popular_majors = [major.strip() for major in majors_match.group(1).split(",")]
            else:
                popular_majors = []

            # acc rate
            acceptance_rate_match = re.search(r"acceptance rate is ([\d.]+)%", desc)
            if acceptance_rate_match:
                acceptance_rate = float(acceptance_rate_match.group(1))
            else:
                acceptance_rate = None
        except:
            print("no desc")
            number_of_students = None
            acceptance_rate = None
            popular_majors = []


        accRate = college_soup.find("span",class_="scalar__value")
        #print(accRate)


        

        # Extract other desired data fields here using BeautifulSoup and regex

        data.append({
            'College':college_name,
            'Rank':college_rank,
            'State':state,
            'Grades': grades_dict,
            'Students':number_of_students,
            'Majors':popular_majors,
            'Acceptance Rate':acceptance_rate

        })

# Create a Pandas DataFrame from the extracted data


df = pd.DataFrame.from_dict(data)


df.to_csv('niche_scraped_colleges.csv')


# Output the DataFrame

