# create the list of schools we want to study
schools = {
    'ironhack': 10828,
    'app-academy': 10525,
    'le-wagon': 10868,
    'ubiqum-code-academy': 11111,
    'udacity': 11118,
}

import re
import pandas as pd
from pandas.io.json import json_normalize
import requests


def get_comments_school(school):
    # create a regex expressionn that will search for the html tags
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

    # create a column in reviews "review_body" that will be populated with another columns created 'body' that will be remove all the html tags
    reviews['review_body'] = reviews['body'].apply(remove_tags)
    # create a column 'school' with the school
    reviews['school'] = school
    # return the table with all the reviews of a defined school
    return reviews


# list comprehension
comments = [get_comments_school(school) for school in schools.keys()]

comments = pd.concat(comments)

from pandas.io.json import json_normalize


def get_school_info(school, school_id):
    # create the URL for each school
    url = 'https://www.switchup.org/chimera/v1/bootcamp-data?mainTemplate=bootcamp-data%2Fdescription&path=%2Fbootcamps%2F' + str(
        school) + '&isDataTarget=false&bootcampId=' + str(
        school_id) + '&logoTag=logo&truncationLength=250&readMoreOmission=...&readMoreText=Read%20More&readLessText=Read%20Less'

    # create a json fil
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
    a, b, c, d = get_school_info(school, id)

    locations_list.append(a)
    courses_list.append(b)
    badges_list.append(c)
    schools_list.append(d)

locations = pd.concat(locations_list)
courses = pd.concat(courses_list)
badges = pd.concat(badges_list)
schools = pd.concat(schools_list)
schools = pd.concat(schools_list)


# functions for data cleaning
def remove_tags_url(x):
    TAG_RE = re.compile("/.*$")
    return TAG_RE.sub('', x)


def remove_tags_html(x):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', x)


def convert_integer(x):
    if type(x) == float:
        x = int(x)
    else:
        x
    return x


# schools data cleaning
schools['description'] = schools['description'].apply(remove_tags_html)
schools['website'] = schools['website'].apply(remove_tags_url)
# schools droping tables
schools = schools.drop(['LogoUrl'], axis=1)

# badges data cleaning
badges['description'] = badges['description'].apply(remove_tags_html)

# comments data cleaning
comments['body'] = comments['body'].apply(remove_tags_html)
comments['graduatingYear'].fillna(0, inplace=True)
comments['graduatingYear']
comments['graduatingYear'] = comments['graduatingYear'].apply(convert_integer)

# comments droping tables
comments = comments.drop(['queryDate'], axis=1)
comments = comments.drop(['user'], axis=1)
comments = comments.drop(['comments'], axis=1)

# Joan course data cleaning
mydict = {}

for x in courses['courses'].unique():
    if x not in mydict.keys():
        mydict[x] = 0
    else:
        continue


def word_finder(keys):
    global mydict

    a = set(['data', 'analytics', 'analyst', 'science', 'python', 'react', 'artificial', 'AI', 'deep', 'machine',
             'learning', 'natural'])
    b = set(['web', 'development', 'android', 'ios', 'java', 'fullstack'])
    c = set(['UX', 'UI', 'design', 'designer'])
    d = set(['software', 'engineer'])

    for key in keys:
        if len(a.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'data analysis/data science' + ' related course'
            # break
        elif len(b.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'web development' + ' related course'
            # break
        elif len(c.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'UX/UI Design' + ' related course'
            # break
        elif len(d.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'Back end development' + ' related course'
            # break
        elif key == "No informations":
            mydict[key] = "No Informations"
        else:
            mydict[key] = 'other courses'

    return mydict


word_finder(list(mydict.keys()))

a = courses['courses']
courses['courses by group'] = a  # create a new column
courses['courses by group'] = courses['courses by group'].replace(mydict)

# identification of online/offline courses
mydict1 = {}
for x in comments['school'].unique():
    if x not in mydict1.keys():
        mydict1[x] = 0
    else:
        continue
mydict1
print(list(mydict1.keys()))


def online_offline(keys):
    global mydict1
    for key in keys:
        if key.lower() == 'ironhack' or key.lower() == 'app-academy':
            mydict1[key] = 'Online/Offline'
        elif key.lower() == 'le-wagon' or key.lower() == 'ubiqum-code-academy':
            mydict1[key] = 'Online'
        elif key.lower() == 'udacity':
            mydict1[key] = 'Offline'
    return mydict1


online_offline(list(mydict1.keys()))
online_offline_column = comments['school']
comments['Online/Offline'] = online_offline_column
comments['Online/Offline'] = comments['Online/Offline'].replace(mydict1)

list_to_drop = ['country.id', 'country.abbrev', 'city.keyword', 'state.id', 'state.name', 'state.abbrev',
                'state.keyword', 'city.id', 'description']
for x in list_to_drop:
    locations = locations.drop([x], axis=1)

courses["index"] = courses.index
courses['courses_id'] = courses['school_id'].apply(str) + "_" + courses["index"].apply(str)
courses['concat'] = courses['school_id'].apply(str) + courses['courses by group']

comments['program'].fillna("No informations", inplace=True)

mydict = {}

for x in comments['program'].unique():
    if x not in mydict.keys():
        mydict[x] = 0
    else:
        continue


def word_finder(keys):
    global mydict

    a = set(['data', 'analytics', 'analyst', 'science', 'python', 'react', 'artificial', 'AI', 'deep', 'machine',
             'learning', 'natural'])
    b = set(['web', 'development', 'android', 'ios', 'java', 'fullstack'])
    c = set(['UX', 'UI', 'design', 'designer'])
    d = set(['software', 'engineer'])

    for key in keys:
        if len(a.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'data analysis/data science' + ' related course'
            # break
        elif len(b.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'web development' + ' related course'
            # break
        elif len(c.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'UX/UI Design' + ' related course'
            # break
        elif len(d.intersection(set(key.lower().split(" ")))) != 0:
            mydict[key] = 'Back end development' + ' related course'
            # break
        elif key == "No informations":
            mydict[key] = "No Informations"
        else:
            mydict[key] = 'other courses'

    return mydict


word_finder(list(mydict.keys()))

a = comments['program']
comments['courses by group'] = a  # create a new column
comments['courses by group'] = comments['courses by group'].replace(mydict)

schools_1 = {
    'ironhack': 10828,
    'app-academy': 10525,
    'le-wagon': 10868,
    'ubiqum-code-academy': 11111,
    'udacity': 11118,
}

comments['school_ID'] = comments['school'].map(schools_1)
comments['concat'] = comments['school_ID'].apply(str) + comments['courses by group']
comments = pd.merge(comments, courses['courses_id'], left_on=comments['concat'], right_on=courses['concat'])
list_to_drop = ['key_0', 'anonymous', 'hostProgramName', 'isAlumni', 'tagline', 'body', 'review_body', 'concat']
for x in list_to_drop:
    comments = comments.drop([x], axis=1)

badges_number = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
badges['badges_id'] = badges_number

list_to_drop = ['index', 'concat']
for x in list_to_drop:
    courses = courses.drop([x], axis=1)

# Pieter lines

# change index
# schools = schools.set_index("website")
# badges = badges.set_index("name")
# import the module
# import pymysql
# from sqlalchemy import create_engine

# create sqlalchemy engine
# engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
#                       .format(user="root",
#                              pw="Albatros93*",
#                              db="ironhack_landscape"))

# Insert whole DataFrame into MySQL
# schools.to_sql('schools', con = engine, if_exists = 'append', chunksize = 1000)
# badges.to_sql('badges', con = engine, if_exists = 'append', chunksize = 1000)
###

#for x in ('badges', 'schools', 'locations', 'courses', 'comments' ):
#    string()
#
##badges.to_csv('/Users/guillaumeaubert/Documents/Ironhack/Module1/Projects/P2_Ironhack_competitive_landscape/badges.csv')
#schools.to_csv('/Users/guillaumeaubert/Documents/Ironhack/Module1/Projects/P2_Ironhack_competitive_landscape/schools.csv')
#locations.to_csv('/Users/guillaumeaubert/Documents/Ironhack/Module1/Projects/P2_Ironhack_competitive_landscape/locations.csv')
#courses.to_csv('/Users/guillaumeaubert/Documents/Ironhack/Module1/Projects/P2_Ironhack_competitive_landscape/courses.csv')
#comments.to_csv('/Users/guillaumeaubert/Documents/Ironhack/Module1/Projects/P2_Ironhack_competitive_landscape/comments.csv')
#
#comments.range
#badges


#badges_number = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7']
#badges['badges_id'] = badges_number

list_ok = ['c'+ str(x) for x in range(len(comments))]
comments['comments_id'] = list_ok

print(list_ok)

len(comments['comments_id'])

comments.to_csv('/Users/guillaumeaubert/Documents/Ironhack/Module1/Projects/P2_Ironhack_competitive_landscape/comments.csv')
