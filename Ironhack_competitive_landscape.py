#create the list of schools we want to study
schools = {
    'ironhack': 10828,
    'app-academy': 10525,
    'springboard': 11035
}

import re
import pandas as pd
from pandas.io.json import json_normalize
import requests


def get_comments_school(school):
    #create a regex expressionn that will search for the html tags
    TAG_RE = re.compile(r'<[^>]+>')
    # defines url to make api call to data -> dynamic with school if you want to scrape competition
    url = "https://www.switchup.org/chimera/v1/school-review-list?mainTemplate=school-review-list&path=%2Fbootcamps%2F" + school + "&isDataTarget=false&page=3&perPage=10000&simpleHtml=true&truncationLength=250"
    # makes get request and converts answer to json
    # url defines the page of all the information, request is made, and information is returned to data variable
    data = requests.get(url).json()
    # converts json to dataframe
    reviews = pd.DataFrame(data['content']['reviews'])

    # aux function to apply regex and remove tags
    def remove_tags(x):
        return TAG_RE.sub('', x)
    #create a column in reviews "review_body" that will be populated with another columns created 'body' that will be remove all the html tags
    reviews['review_body'] = reviews['body'].apply(remove_tags)
    # create a column 'school' with the school
    reviews['school'] = school
    #return the table with all the reviews of a defined school
    return reviews




#list comprehension
comments=[get_comments_school(school) for school in schools.keys()]

comments = pd.concat(comments)

from pandas.io.json import json_normalize


def get_school_info(school, school_id):
    #create the URL for each school
    url = 'https://www.switchup.org/chimera/v1/bootcamp-data?mainTemplate=bootcamp-data%2Fdescription&path=%2Fbootcamps%2F' + str(
        school) + '&isDataTarget=false&bootcampId=' + str(
        school_id) + '&logoTag=logo&truncationLength=250&readMoreOmission=...&readMoreText=Read%20More&readLessText=Read%20Less'

    #create a json fil
    data = requests.get(url).json()

    data.keys()

    courses = data['content']['courses']
    courses_df = pd.DataFrame(courses, columns=['courses'])

    locations = data['content']['locations']
    locations_df = json_normalize(locations)

    badges_df = pd.DataFrame(data['content']['meritBadges'])

    website = data['content']['webaddr']
    description = data['content']['description']
    logoUrl = data['content']['logoUrl']
    school_df = pd.DataFrame([website, description, logoUrl]).T
    school_df.columns = ['website', 'description', 'LogoUrl']

    locations_df['school'] = school
    courses_df['school'] = school
    badges_df['school'] = school
    school_df['school'] = school

    # how could you write a similar block of code to the above in order to record the school ID?

    locations_df['school_id'] = school_id
    courses_df['school_id'] = school_id
    badges_df['school_id'] = school_id
    school_df['school_id'] = school_id

    return locations_df, courses_df, badges_df, school_df


locations_list = []
courses_list = []
badges_list = []
schools_list = []

for school, id in schools.items():
    print(school)
    a, b, c, d = get_school_info(school, id)

    locations_list.append(a)
    courses_list.append(b)
    badges_list.append(c)
    schools_list.append(d)

locations = pd.concat(locations_list)
locations

courses = pd.concat(courses_list)
courses.head(10)

badges = pd.concat(badges_list)
badges.head()

schools = pd.concat(schools_list)
schools.head()


print(schools.head())