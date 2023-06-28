import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib


## Stack Overflow ##



# Define the URL of the website to scrape

# Extract data from each college page
data = []
header = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15,",
    # might need to find your own user agent
    'referer':'https://www.niche.com/'
    }


for i in range (1,109):
	nicheURL = 'https://www.niche.com/colleges/search/best-colleges/?page='+str(i)
    nichePage = requests.get(nicheURL,headers=header)
    soup = BeautifulSoup(nichePage.content,"html.parser")
    

    #with open("/Users/arinjaff/Downloads/niche.html", 'rb') as fp:
     #   soup = BeautifulSoup(fp)

        # Find all the links to college pages
    college_links = soup.find_all("a", class_="search-result__link")

    #print(college_links)
    # Ads


    college_urls = []
    for link in college_links:
        href = link.get("href")
        if href and re.search(r"/colleges/\S+", href):
            if not link.find("h2", string="Sponsored Result"):
                if (href != 'https://www.niche.com/colleges/university-of-north-carolina-system/') and (href != 'https://www.niche.com/colleges/university-of-the-potomac-system/'):
                    college_urls.append(href)
            else:
                print("excluded" + href)
    #print("URLS:",college_urls)
    for college_url in college_urls:
        
        print("CURRENT SCHOOL:",college_url)

        
        newUrl = 'http://webcache.googleusercontent.com/search?q=cache:'+college_url
        college_response = requests.get(newUrl,headers=header)

        #print(college_response)
        
        college_response = requests.get(newUrl)
        college_soup = BeautifulSoup(college_response.content, "html.parser")
        
        print(college_response.content)

        #print(college_response.content)

        
        college = college_soup.find("div", class_="postcard__content postcard__content--primary")
        if college is not None:
            college = college.text.strip()
            college_name = college.split("#")[0].strip()
            college_name = college.split("This")[0].strip()
            state_match = re.search(r",\s*([A-Z]{2})", college)
            state = state_match if state_match else None
        else:
            print("hit captcha")
            state = None


        print("couldn't find college name")
        college_name = college_url

        # Extract college rank
        college_rank = college_urls.index(college_url)+1

        # Extract state


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


df.to_csv('niche_colleges.csv')


# Output the DataFrame

