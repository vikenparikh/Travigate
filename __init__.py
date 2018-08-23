# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 02:27:43 2018

@author: Viken
"""
################Imports#####################
from flask import Flask,request,render_template,redirect,url_for
import urllib.request
import pymysql
import json
import pandas as pd
import numpy as np
#import pylab as pl
import os
import uuid
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
import seaborn as sns
from sklearn import metrics
from kmodes.kmodes import KModes
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, IMAGES
from keras.preprocessing import image
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
import Images_TrainAndSaveModel as tsm
import images_scrapper as im
from sklearn.externals import joblib
from threading import Thread
from werkzeug.utils import secure_filename

absoultepath= "/home/ubuntu/Travigate/"
################Imports#####################
################Initializing data#####################
database = pymysql.connect (host="travigate.ckwuo5gm9cp9.ap-south-1.rds.amazonaws.com", port = 3306 ,user = "vikenparikh", passwd = "vikenparikh", db = "Travigate")
#database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate")
dataset_initial = pd.read_sql('Select * from user;', con=database)
pd.options.mode.chained_assignment = None
dataset=dataset_initial
dataset['Foodie']=0
dataset['60+ Traveler']=0
dataset['Like a Local']=0
dataset['Nature Lover']=0
dataset['Urban Explorer']=0
dataset['Luxury Traveller']=0
dataset['Shopping Fanatic']=0
dataset['Peace and Quiet Seeker']=0
dataset['Thrill Seeker']=0
dataset['Thrifty Traveller']=0
dataset['Beach Goer']=0
dataset['Family Hoilday Maker']=0
dataset['Nightlife Seeker']=0
dataset['Art and Architecture Lover']=0
dataset['Vegetarian']=0
dataset['History Buff']=0
dataset['Trendsetter']=0

for j,row in dataset.iterrows() :
    p=str(dataset['travelStyle'][j])
    if p.find("Default") == -1:
        blank=0
    else:
        if p.find("Foodie") != -1:
            dataset['Foodie'][j]=1
        if p.find("60+ Traveler") != -1:
            dataset['60+ Traveler'][j]=1
        if p.find("Like a Local") != -1:
            dataset['Like a Local'][j]=1
        if p.find("Nature Lover") != -1:
            dataset['Nature Lover'][j]=1
        if p.find("Urban Explorer") != -1:
            dataset['Urban Explorer'][j]=1
        if p.find("Luxury Traveller") != -1:
            dataset['Luxury Traveller'][j]=1
        if p.find("Shopping Fanatic") != -1:
            dataset['Shopping Fanatic'][j]=1
        if p.find("Peace and Quiet Seeker") != -1:
            dataset['Peace and Quiet Seeker'][j]=1
        if p.find("Thrill Seeker") != -1:
            dataset['Thrill Seeker'][j]=1
        if p.find("Thrifty Traveller") != -1:
            dataset['Thrifty Traveller'][j]=1
        if p.find("Beach Goer") != -1:
            dataset['Beach Goer'][j]=1
        if p.find("Family Hoilday Maker") != -1:
            dataset['Family Hoilday Maker'][j]=1
        if p.find("Nightlife Seeker") != -1:
            dataset['Nightlife Seeker'][j]=1
        if p.find("Art and Architecture Lover") != -1:
            dataset['Art and Architecture Lover'][j]=1
        if p.find("Vegetarian") != -1:
            dataset['Vegetarian'][j]=1
        if p.find("History Buff") != -1:
            dataset['History Buff'][j]=1
        if p.find("Trendsetter") != -1:
            dataset['Trendsetter'][j]=1
################Initializing data#####################

################Clustering#####################
#clustering of hotels
train_inde_hotels = dataset
dataset_reviews_hotels = pd.read_sql('Select * from reviews;', con=database)
X_Hotels = train_inde_hotels[['username','ageRange','gender','numHotelsReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
taObjectCity_reviews_full_merged_hotels = pd.merge(dataset_reviews_hotels,train_inde_hotels,how='left',left_on=['username'], right_on=['username'])
taObjectCity_reviews_full_merged_hotels.fillna(0, inplace=True)
#km_hotels = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
X_taObjectCity_reviews_full_merged_features_train_hotels = taObjectCity_reviews_full_merged_hotels[['ageRange','gender','numHotelsReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
#clusters_hotels = km_hotels.fit_predict(X_taObjectCity_reviews_full_merged_features_train_hotels[:].as_matrix())
#print(km_hotels.cluster_centroids_)
#km_hotels_filename = 'km_hotels_model.sav'
#joblib.dump(km_hotels, km_hotels_filename)
km_hotels_filename = 'km_hotels_model.sav'
km_hotels = joblib.load(km_hotels_filename)



#clustering of attractions
train_inde_attractions = dataset
dataset_reviews_attractions = pd.read_sql('Select * from reviews;', con=database)
X_Attract = train_inde_attractions[['username','ageRange','gender','numAttractReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
taObjectCity_reviews_full_merged_attractions = pd.merge(dataset_reviews_attractions,train_inde_attractions,how='left',left_on=['username'], right_on=['username'])
taObjectCity_reviews_full_merged_attractions.fillna(0, inplace=True)
#km_attractions = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
X_taObjectCity_reviews_full_merged_features_train_attractions = taObjectCity_reviews_full_merged_attractions[['ageRange','gender','numAttractReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
#clusters_attractions = km_attractions.fit_predict(X_taObjectCity_reviews_full_merged_features_train_attractions[:].as_matrix())
#print(km_attractions.cluster_centroids_)
#km_attractions_filename = 'km_attractions_model.sav'
#joblib.dump(km_attractions, km_attractions_filename)
km_attractions_filename = 'km_attractions_model.sav'
km_attractions = joblib.load(km_attractions_filename)



#clustering of restaurants
train_inde_restaurants = dataset
dataset_reviews_restaurants = pd.read_sql('Select * from reviews;', con=database)
X_Rest = train_inde_restaurants[['username','ageRange','gender','numRestReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
taObjectCity_reviews_full_merged_restaurants = pd.merge(dataset_reviews_restaurants,train_inde_restaurants,how='left',left_on=['username'], right_on=['username'])
taObjectCity_reviews_full_merged_restaurants.fillna(0, inplace=True)
#km_restaurants = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
X_taObjectCity_reviews_full_merged_features_train_restaurants = taObjectCity_reviews_full_merged_restaurants[['ageRange','gender','numRestReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
#clusters_restaurants = km_restaurants.fit_predict(X_taObjectCity_reviews_full_merged_features_train_restaurants[:].as_matrix())
#print(km_restaurants.cluster_centroids_)
#km_restaurants_filename = 'km_restaurants_model.sav'
#joblib.dump(km_attractions, km_restaurants_filename)
km_restaurants_filename = 'km_restaurants_model.sav'
km_restaurants = joblib.load(km_restaurants_filename)

################Clustering#####################

################Initialize Flask App#####################
app = Flask(__name__)
CORS(app)

photos = UploadSet('photos', IMAGES)
app.config['UPLOAD_FOLDER'] = absoultepath+"upload/"
#configure_uploads(app, photos)

#photos = UploadSet('photos', IMAGES)
#UPLOAD_FOLDER = '/uploads'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#configure_uploads(app, photos)
################Initialize Flask App#####################

################Login#####################
@app.route('/Login', methods=['GET','POST'])
def ThisLogin():
    if 'Username' in request.args:
        username = request.args.get('Username')
        password = request.args.get('Password')
        #username="Viken"
        #password="parikh"
        #username="0BKI0"
        #password="15191892"
        #database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate")
        database = pymysql.connect (host="travigate.ckwuo5gm9cp9.ap-south-1.rds.amazonaws.com", port = 3306 ,user = "vikenparikh", passwd = "vikenparikh", db = "Travigate")
        users = pd.read_sql('Select * from user;', con=database)    
        user = users.loc[(users['username'] == username) & (users['password'] == password)]
        user=user.as_matrix()
        user_exist=0
        if user.any():
            user_exist=1
            ageRange=user[0][2]
            gender=user[0][3]
            numHotelsReviews=user[0][4]
            numRestReviews=user[0][5]
            numAttractReviews=user[0][6]
            num1irstToReview=user[0][7]
            numRatings=user[0][8]
            numPhotos=user[0][9]
            num1orumPosts=user[0][10]
            numArticles=user[0][11]
            numCitiesBeen=user[0][12]
            totalPoints=user[0][13]
            contribLevel=user[0][14]
            numHelp1ulVotes=user[0][15]
            reviewerBadge=user[0][16]
            travelStyle=user[0][17]
            message="Welcome "+username
            city = pd.read_sql('Select * from reviews;', con=database)
            places =city['taObjectCity']
            keywords = []
            for x in places:
                if x not in keywords:
                    keywords.append(x)
            keywords=sorted(keywords)
            dic={}
            dic['taObjectCity'] = keywords
            data={"response": 
                [{"success":"1"},
                {"message":message}, 
                {"username":username},
                {"ageRange":ageRange},
                {"gender":gender},
                {"numHotelsReviews":numHotelsReviews},
                {"numRestReviews":numRestReviews},
                {"numAttractReviews":numAttractReviews},
                {"num1irstToReview":num1irstToReview},
                {"numRatings":numRatings},
                {"numPhotos":numPhotos},
                {"num1orumPosts":num1orumPosts},
                {"numArticles":numArticles},
                {"numCitiesBeen":numCitiesBeen},
                {"totalPoints":totalPoints},
                {"contribLevel":contribLevel},
                {"numHelp1ulVotes":numHelp1ulVotes},
                {"reviewerBadge":reviewerBadge},
                {"travelStyle":travelStyle},
                {"cities":dic}] }
            #data = cur.fetchall()
            return json.dumps(data)
        if user_exist==0:
            data={"response": [ {"success":"0"} , {"message":"User doesnt exist or password incorrect"} ] }
            return json.dumps(data)
    else:
        data={"response": [ {"success":"1"} , {"message":"User Found"}] }
        return json.dumps(data)

################Login#####################

################Register#####################
@app.route('/Register', methods=['GET','POST'])
def Register():
    if 'Username' in request.args:
        username = request.args.get('Username')
        password = request.args.get('Password')
        if ((len(username)>3)&(len(password)>3)): 
            #username="Viken"
            #password="parikh"
            #username="0BKI0"
            #password="15191892"
            #database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate")
            database = pymysql.connect (host="travigate.ckwuo5gm9cp9.ap-south-1.rds.amazonaws.com", port = 3306 ,user = "vikenparikh", passwd = "vikenparikh", db = "Travigate", autocommit=True)
            users = pd.read_sql('Select * from user;', con=database)    
            user = users.loc[(users['username'] == username) & (users['password'] == password)]
            user=user.as_matrix()
            user_exist=0
            if user.any():
                user_exist=1
                data={"response": [ {"success":"0"} , {"message":"Username exists. Try to login or try register with a different username."} ] }
                return json.dumps(data)
            if user_exist==0:
                ageRange=request.args.get('ageRange')
                gender=request.args.get('gender')
                numHotelsReviews=request.args.get('numHotelsReviews')
                numRestReviews=request.args.get('numRestReviews')
                numAttractReviews=request.args.get('numAttractReviews')
                num1irstToReview=request.args.get('num1irstToReview')
                numRatings=request.args.get('numRatings')
                numPhotos=request.args.get('numPhotos')
                num1orumPosts=request.args.get('num1orumPosts')
                numArticles=request.args.get('numArticles')
                numCitiesBeen=request.args.get('numCitiesBeen')
                totalPoints=request.args.get('totalPoints')
                contribLevel=request.args.get('contribLevel')
                numHelp1ulVotes=request.args.get('numHelp1ulVotes')
                reviewerBadge=request.args.get('reviewerBadge')
                travelStyle=request.args.get('travelStyle')
                query=""
                query='Insert INTO user (username, password, ageRange, gender, numHotelsReviews, numRestReviews, numAttractReviews, num1irstToReview, numRatings, numPhotos, num1orumPosts, numArticles, numCitiesBeen, totalPoints, contribLevel, numHelp1ulVotes, reviewerBadge, travelStyle)'
                query=query+"VALUES ("
                query=query+'"'+str(username)+'"'+" , "
                query=query+'"'+str(password)+'"'+" , "
                query=query+str(ageRange)+" , "
                query=query+str(gender)+" , "
                query=query+str(numHotelsReviews)+" , "
                query=query+str(numRestReviews)+" , "
                query=query+str(numAttractReviews)+" , "
                query=query+str(num1irstToReview)+" , "
                query=query+str(numRatings)+" , "
                query=query+str(numPhotos)+" , "
                query=query+str(num1orumPosts)+" , "
                query=query+str(numArticles)+" , "
                query=query+str(numCitiesBeen)+" , "
                query=query+str(totalPoints)+" , "
                query=query+str(contribLevel)+" , "
                query=query+str(numHelp1ulVotes)+" , "
                query=query+str(reviewerBadge)+" , "
                query=query+'"'+str(travelStyle)+'"'+");"
                cur = database.cursor()
                registered=cur.execute(query)
                if registered==1:
                    reInitialiseData()
                    data={"response": [ {"success":"1"} , {"message":"User Registered Successfully"} ] }
                    return json.dumps(data)
                else:
                    data={"response": [ {"success":"0"} , {"message":"Error Registering user, try again"} ] }
                    return json.dumps(data)
        else:
            data={"response": [ {"success":"0"} , {"message":"Username and password length should be greater than 3"}] }
            return json.dumps(data)
    else:
        data={"response": [ {"success":"0"} , {"message":"Username not Found"}] }
        return json.dumps(data)

################Register#####################

def reInitialiseData():
################Reinitialse Data#####################

################Initializing data#####################
    global database
    database = pymysql.connect (host="travigate.ckwuo5gm9cp9.ap-south-1.rds.amazonaws.com", port = 3306 ,user = "vikenparikh", passwd = "vikenparikh", db = "Travigate")
    #database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate")
    global dataset_initial
    dataset_initial = pd.read_sql('Select * from user;', con=database)
    pd.options.mode.chained_assignment = None
    global dataset
    dataset=dataset_initial
    dataset['Foodie']=0
    dataset['60+ Traveler']=0
    dataset['Like a Local']=0
    dataset['Nature Lover']=0
    dataset['Urban Explorer']=0
    dataset['Luxury Traveller']=0
    dataset['Shopping Fanatic']=0
    dataset['Peace and Quiet Seeker']=0
    dataset['Thrill Seeker']=0
    dataset['Thrifty Traveller']=0
    dataset['Beach Goer']=0
    dataset['Family Hoilday Maker']=0
    dataset['Nightlife Seeker']=0
    dataset['Art and Architecture Lover']=0
    dataset['Vegetarian']=0
    dataset['History Buff']=0
    dataset['Trendsetter']=0
    
    for j,row in dataset.iterrows() :
        p=str(dataset['travelStyle'][j])
        if p.find("Default") == -1:
            blank=0
        else:
            if p.find("Foodie") != -1:
                dataset['Foodie'][j]=1
            if p.find("60+ Traveler") != -1:
                dataset['60+ Traveler'][j]=1
            if p.find("Like a Local") != -1:
                dataset['Like a Local'][j]=1
            if p.find("Nature Lover") != -1:
                dataset['Nature Lover'][j]=1
            if p.find("Urban Explorer") != -1:
                dataset['Urban Explorer'][j]=1
            if p.find("Luxury Traveller") != -1:
                dataset['Luxury Traveller'][j]=1
            if p.find("Shopping Fanatic") != -1:
                dataset['Shopping Fanatic'][j]=1
            if p.find("Peace and Quiet Seeker") != -1:
                dataset['Peace and Quiet Seeker'][j]=1
            if p.find("Thrill Seeker") != -1:
                dataset['Thrill Seeker'][j]=1
            if p.find("Thrifty Traveller") != -1:
                dataset['Thrifty Traveller'][j]=1
            if p.find("Beach Goer") != -1:
                dataset['Beach Goer'][j]=1
            if p.find("Family Hoilday Maker") != -1:
                dataset['Family Hoilday Maker'][j]=1
            if p.find("Nightlife Seeker") != -1:
                dataset['Nightlife Seeker'][j]=1
            if p.find("Art and Architecture Lover") != -1:
                dataset['Art and Architecture Lover'][j]=1
            if p.find("Vegetarian") != -1:
                dataset['Vegetarian'][j]=1
            if p.find("History Buff") != -1:
                dataset['History Buff'][j]=1
            if p.find("Trendsetter") != -1:
                dataset['Trendsetter'][j]=1
################Initializing data#####################
    
################Clustering#####################
    #clustering of hotels
    global train_inde_hotels,dataset_reviews_hotels,X_Hotels,taObjectCity_reviews_full_merged_hotels,X_taObjectCity_reviews_full_merged_features_train_hotels,km_hotels_filename,km_hotels
    train_inde_hotels = dataset
    dataset_reviews_hotels = pd.read_sql('Select * from reviews;', con=database)
    X_Hotels = train_inde_hotels[['username','ageRange','gender','numHotelsReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
    taObjectCity_reviews_full_merged_hotels = pd.merge(dataset_reviews_hotels,train_inde_hotels,how='left',left_on=['username'], right_on=['username'])
    taObjectCity_reviews_full_merged_hotels.fillna(0, inplace=True)
    #km_hotels = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
    X_taObjectCity_reviews_full_merged_features_train_hotels = taObjectCity_reviews_full_merged_hotels[['ageRange','gender','numHotelsReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
    #clusters_hotels = km_hotels.fit_predict(X_taObjectCity_reviews_full_merged_features_train_hotels[:].as_matrix())
    #print(km_hotels.cluster_centroids_)
    #km_hotels_filename = 'km_hotels_model.sav'
    #joblib.dump(km_hotels, km_hotels_filename)
    km_hotels_filename = 'km_hotels_model.sav'
    km_hotels = joblib.load(km_hotels_filename)
    
    
    global train_inde_attractions,dataset_reviews_attractions,X_Attract,taObjectCity_reviews_full_merged_attractions,X_taObjectCity_reviews_full_merged_features_train_attractions,km_attractions_filename,km_attractions
    #clustering of attractions
    train_inde_attractions = dataset
    dataset_reviews_attractions = pd.read_sql('Select * from reviews;', con=database)
    X_Attract = train_inde_attractions[['username','ageRange','gender','numAttractReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
    taObjectCity_reviews_full_merged_attractions = pd.merge(dataset_reviews_attractions,train_inde_attractions,how='left',left_on=['username'], right_on=['username'])
    taObjectCity_reviews_full_merged_attractions.fillna(0, inplace=True)
    #km_attractions = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
    X_taObjectCity_reviews_full_merged_features_train_attractions = taObjectCity_reviews_full_merged_attractions[['ageRange','gender','numAttractReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
    #clusters_attractions = km_attractions.fit_predict(X_taObjectCity_reviews_full_merged_features_train_attractions[:].as_matrix())
    #print(km_attractions.cluster_centroids_)
    #km_attractions_filename = 'km_attractions_model.sav'
    #joblib.dump(km_attractions, km_attractions_filename)
    km_attractions_filename = 'km_attractions_model.sav'
    km_attractions = joblib.load(km_attractions_filename)
    
    
    global train_inde_restaurants,dataset_reviews_restaurants,X_Rest,taObjectCity_reviews_full_merged_restaurants,X_taObjectCity_reviews_full_merged_features_train_restaurants,km_restaurants_filename,km_restaurants
    #clustering of restaurants
    train_inde_restaurants = dataset
    dataset_reviews_restaurants = pd.read_sql('Select * from reviews;', con=database)
    X_Rest = train_inde_restaurants[['username','ageRange','gender','numRestReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
    taObjectCity_reviews_full_merged_restaurants = pd.merge(dataset_reviews_restaurants,train_inde_restaurants,how='left',left_on=['username'], right_on=['username'])
    taObjectCity_reviews_full_merged_restaurants.fillna(0, inplace=True)
    #km_restaurants = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
    X_taObjectCity_reviews_full_merged_features_train_restaurants = taObjectCity_reviews_full_merged_restaurants[['ageRange','gender','numRestReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
    #clusters_restaurants = km_restaurants.fit_predict(X_taObjectCity_reviews_full_merged_features_train_restaurants[:].as_matrix())
    #print(km_restaurants.cluster_centroids_)
    #km_restaurants_filename = 'km_restaurants_model.sav'
    #joblib.dump(km_attractions, km_restaurants_filename)
    km_restaurants_filename = 'km_restaurants_model.sav'
    km_restaurants = joblib.load(km_restaurants_filename)
    
################Clustering#####################
    
################Reinititialise data#####################

################Comment#####################
@app.route('/Comment', methods=['GET','POST'])
def Comment():
    if 'Username' in request.args:
        username = request.args.get('Username')
        '''
        username="Vike1"
        type="Hotels"
        taObjectCity="Stockholm"
        taObject="Radisson Blu Royal Viking Hotel, Stockholm"
        rating="4"
        helpfulness="1"
        total_points="101"
        date="0000-00-00"
        title="Good Choice and would be suitable for a family"
        text="Decent Hotel next to station so good location for ..."
        taObjectUrl="http://www.tripadvisor.com/Hotel_Review-g189852-d2..."
        '''
        #database = pymysql.connect (host="localhost", user = "root", passwd = "", db = "travigate")
        database = pymysql.connect (host="travigate.ckwuo5gm9cp9.ap-south-1.rds.amazonaws.com", port = 3306 ,user = "vikenparikh", passwd = "vikenparikh", db = "Travigate")
        users = pd.read_sql('Select * from user;', con=database)    
        user = users.loc[(users['username'] == username)]
        user=user.as_matrix()
        user_exist=0
        if user.any():
            type=request.args.get('type')
            taObjectCity=request.args.get('taObjectCity')
            taObject=request.args.get('taObject')
            rating=request.args.get('rating')
            title=request.args.get('title')
            text=request.args.get('text')
            helpfulness=request.args.get('helpfulness')
            total_points=request.args.get('total_points')
            date="0000-00-00"
            taObjectUrl=request.args.get('taObjectUrl')
            query=""
            query='Insert INTO reviews (username, type, taObjectCity, taObject, rating, helpfulness, total_points, date, title, text, taObjectUrl)'
            query=query+"VALUES ("
            query=query+'"'+str(username)+'"'+" , "
            query=query+'"'+str(type)+'"'+" , "
            query=query+'"'+str(taObjectCity)+'"'+" , "
            query=query+'"'+str(taObject)+'"'+" , "
            query=query+str(rating)+" , "
            query=query+str(helpfulness)+" , "
            query=query+str(total_points)+" , "
            query=query+'"'+str(date)+'"'+" , "
            query=query+'"'+str(title)+'"'+" , "
            query=query+'"'+str(text)+'"'+" , "
            query=query+'"'+str(taObjectUrl)+'"'+");"
            cur = database.cursor()
            Comment=cur.execute(query)
            if Comment==1:
                data={"response": [ {"success":"1"} , {"message":"Review Successfully Posted"} ] }
                return json.dumps(data)
            else:
                data={"response": [ {"success":"0"} , {"message":"Error Posting the review, try again"} ] }
                return json.dumps(data)
        if user_exist==0:
            data={"response": [ {"success":"0"} , {"message":"User not logged in!"} ] }
            return json.dumps(data)
    else:
        data={"response": [ {"success":"0"} , {"message":"User not logged in!"}] }
        return json.dumps(data)

################Comment#####################

################Suggest_Places#####################
@app.route('/Dashboard', methods=['GET','POST'])
def Dashboard():
    if 'Username' in request.args:
        username = request.args.get('Username')
        type1 = request.args.get('type')
        taObjectCity = request.args.get('taObjectCity')
        '''
        ageRange = request.args.get('ageRange')
        gender= request.args.get('gender')
        numHotelsReviews= request.args.get('numHotelsReviews')
        numRestReviews= request.args.get('numRestReviews')
        numAttractReviews= request.args.get('numAttractReviews')
        num1irstToReview= request.args.get('num1irstToReview')
        numRatings= request.args.get('numRatings')
        numPhotos= request.args.get('numPhotos')
        num1orumPosts= request.args.get('num1orumPosts')
        numArticles= request.args.get('numArticles')
        numCitiesBeen= request.args.get('numCitiesBeen')
        totalPoints= request.args.get('totalPoints')
        contribLevel= request.args.get('contribLevel')
        numHelp1ulVotes= request.args.get('numHelp1ulVotes')
        reviewerBadge= request.args.get('reviewerBadge')
        travelStyle= request.args.get('travelStyle')
        '''
        '''
        username="Viken"
        type1="Attractions"
        taObjectCity = "Mumbai (Bombay)"
        ageRange = 4
        gender= 1
        numHotelsReviews= 10
        numRestReviews= 1
        numAttractReviews= 1
        num1irstToReview= 0
        numRatings= 6
        numPhotos= 0
        num1orumPosts= 0
        numArticles= 0
        numCitiesBeen= 8
        totalPoints= 1240
        contribLevel= 3
        numHelp1ulVotes= 10
        reviewerBadge= 2
        travelStyle= "0"
        '''
        if type1=="Hotels":
            try:
                taObjectCity_reviews_hotels = dataset_reviews_hotels.loc[(dataset_reviews_hotels['taObjectCity'] == taObjectCity) & (dataset_reviews_hotels['type'] == type1)]
                taObjectCity_reviews_hotels = taObjectCity_reviews_hotels[['username','taObject','rating','helpfulness','title','text']]
                taObjectCity_reviews_output_merged_predict_hotels = pd.merge(taObjectCity_reviews_hotels, X_Hotels,how='left',left_on=['username'], right_on=['username'])
                taObjectCity_reviews_output_merged_predict_hotels.fillna(0, inplace=True)
                taObjectCity_reviews_test_hotels=taObjectCity_reviews_output_merged_predict_hotels[['ageRange','gender','numHotelsReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
                taObjectCity_reviews_test_hotels.fillna(0, inplace=True)
                taObjectCity_reviews_output_merged_predict_hotels['similarity']=km_hotels.predict(taObjectCity_reviews_test_hotels)
                user_attributes_hotels=train_inde_hotels.loc[(train_inde_hotels['username'] == username)]
                user_predict_attributes_hotels=user_attributes_hotels[['ageRange','gender','numHotelsReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
                user_predict_attributes_hotels.fillna(0, inplace=True)
                user_predict_attributes_hotels['similarity']=km_hotels.predict(user_predict_attributes_hotels)
                taObjectCity_reviews_output_places_hotels = taObjectCity_reviews_output_merged_predict_hotels.groupby(['taObject'])['similarity'].mean().reset_index(name='similarity')
                X_places=[]
                X_places_other=[]
                j=0
                user_predict_attributes_hotels_list=user_predict_attributes_hotels['similarity'].values.tolist()
                for i in taObjectCity_reviews_output_places_hotels.taObject:
                    #taObjectCity_reviews_output_places['similarity'][j]=int(taObjectCity_reviews_output_places['similarity'][j])
                    if(int(taObjectCity_reviews_output_places_hotels['similarity'][j])==user_predict_attributes_hotels_list[0]):
                       #print("yes")
                       X_places.append(taObjectCity_reviews_output_places_hotels.taObject[j])
                    j+=1
                j=0
                for i in taObjectCity_reviews_output_places_hotels.taObject:
                    #taObjectCity_reviews_output_places_hotels['similarity'][j]=int(taObjectCity_reviews_output_places_hotels['similarity'][j])
                    if(int(taObjectCity_reviews_output_places_hotels['similarity'][j])!=user_predict_attributes_hotels_list[0]):
                        #print("no")
                        X_places_other.append(taObjectCity_reviews_output_places_hotels.taObject[j])
                    j+=1
                dic={}
                dic['places'] = X_places
                dic1={}
                dic1['places_other'] = X_places_other
                if not dic:
                    if not dic1:
                        data = {"response": [ {"success":"0"} , {"message":"No places found"}] }
                        return json.dumps(data)
                else:    
                    places1={"response": [ {"success":"1"} ,{"message":"places fetched"}, {"places":dic}, {"places_other":dic1}] }
                    return json.dumps(places1)
            except:
                data = {"response": [ {"success":"0"} , {"message":"City Not in our database"}] }
                return json.dumps(data)


        elif type1=="Attractions":
            try:
                print("Yes")
                taObjectCity_reviews_attractions = dataset_reviews_attractions.loc[(dataset_reviews_attractions['taObjectCity'] == taObjectCity) & (dataset_reviews_attractions['type'] == type1)]
                taObjectCity_reviews_attractions = taObjectCity_reviews_attractions[['username','taObject','rating','helpfulness','title','text']]
                taObjectCity_reviews_output_merged_predict_attractions = pd.merge(taObjectCity_reviews_attractions, X_Attract,how='left',left_on=['username'], right_on=['username'])
                taObjectCity_reviews_output_merged_predict_attractions.fillna(0, inplace=True)
                taObjectCity_reviews_test_attractions=taObjectCity_reviews_output_merged_predict_attractions[['ageRange','gender','numAttractReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
                taObjectCity_reviews_test_attractions.fillna(0, inplace=True)
                taObjectCity_reviews_output_merged_predict_attractions['similarity']=km_attractions.predict(taObjectCity_reviews_test_attractions)
                user_attributes_attractions=train_inde_attractions.loc[(train_inde_attractions['username'] == username)]
                user_predict_attributes_attractions=user_attributes_attractions[['ageRange','gender','numAttractReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
                user_predict_attributes_attractions.fillna(0, inplace=True)
                user_predict_attributes_attractions['similarity']=km_attractions.predict(user_predict_attributes_attractions)
                taObjectCity_reviews_output_places_attractions = taObjectCity_reviews_output_merged_predict_attractions.groupby(['taObject'])['similarity'].mean().reset_index(name='similarity')
                X_places=[]
                X_places_other=[]
                j=0
                user_predict_attributes_attractions_list=user_predict_attributes_attractions['similarity'].values.tolist()
                for i in taObjectCity_reviews_output_places_attractions.taObject:
                    #taObjectCity_reviews_output_places_attractions['similarity'][j]=int(taObjectCity_reviews_output_places_attractions['similarity'][j])
                    if(int(taObjectCity_reviews_output_places_attractions['similarity'][j])==user_predict_attributes_attractions_list[0]):
                       #print("yes")
                       X_places.append(taObjectCity_reviews_output_places_attractions.taObject[j])
                    j+=1
                j=0
                for i in taObjectCity_reviews_output_places_attractions.taObject:
                    #taObjectCity_reviews_output_places_attractions['similarity'][j]=int(taObjectCity_reviews_output_places_attractions['similarity'][j])
                    if(int(taObjectCity_reviews_output_places_attractions['similarity'][j])!=user_predict_attributes_attractions_list[0]):
                        #print("no")
                        X_places_other.append(taObjectCity_reviews_output_places_attractions.taObject[j])
                    j+=1
                dic={}
                dic['places'] = X_places
                dic1={}
                dic1['places_other'] = X_places_other
                if not dic:
                    if not dic1:
                        data = {"response": [ {"success":"0"} , {"message":"No places found"}] }
                        return json.dumps(data)
                else:    
                    places1={"response": [ {"success":"1"} ,{"message":"places fetched"}, {"places":dic}, {"places_other":dic1}] }
                    return json.dumps(places1)
            except:
                data = {"response": [ {"success":"0"} , {"message":"City Not in our database"}] }
                return json.dumps(data)
            
        elif type1=="Restaurants":
            try:
                taObjectCity_reviews_restaurants = dataset_reviews_restaurants.loc[(dataset_reviews_restaurants['taObjectCity'] == taObjectCity) & (dataset_reviews_restaurants['type'] == type1)]
                taObjectCity_reviews_restaurants = taObjectCity_reviews_restaurants[['username','taObject','rating','helpfulness','title','text']]
                taObjectCity_reviews_output_merged_predict_restaurants = pd.merge(taObjectCity_reviews_restaurants, X_Rest,how='left',left_on=['username'], right_on=['username'])
                taObjectCity_reviews_output_merged_predict_restaurants.fillna(0, inplace=True)
                taObjectCity_reviews_test_restaurants=taObjectCity_reviews_output_merged_predict_restaurants[['ageRange','gender','numRestReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
                taObjectCity_reviews_test_restaurants.fillna(0, inplace=True)
                taObjectCity_reviews_output_merged_predict_restaurants['similarity']=km_restaurants.predict(taObjectCity_reviews_test_restaurants)
                user_attributes_restaurants=train_inde_restaurants.loc[(train_inde_restaurants['username'] == username)]
                user_predict_attributes_restaurants=user_attributes_restaurants[['ageRange','gender','numRestReviews','num1irstToReview','numRatings','numPhotos','num1orumPosts','numArticles','numCitiesBeen','totalPoints','contribLevel','numHelp1ulVotes','reviewerBadge','Foodie','60+ Traveler','Like a Local','Nature Lover','Urban Explorer','Luxury Traveller','Shopping Fanatic','Peace and Quiet Seeker','Thrill Seeker','Thrifty Traveller','Beach Goer','Family Hoilday Maker','Nightlife Seeker','Art and Architecture Lover','Vegetarian','History Buff','Trendsetter']]
                user_predict_attributes_restaurants.fillna(0, inplace=True)
                user_predict_attributes_restaurants['similarity']=km_restaurants.predict(user_predict_attributes_restaurants)
                taObjectCity_reviews_output_places_restaurants = taObjectCity_reviews_output_merged_predict_restaurants.groupby(['taObject'])['similarity'].mean().reset_index(name='similarity')
                X_places=[]
                X_places_other=[]
                j=0
                user_predict_attributes_restaurants_list=user_predict_attributes_restaurants['similarity'].values.tolist()
                for i in taObjectCity_reviews_output_places_restaurants.taObject:
                    #taObjectCity_reviews_output_places_restaurants['similarity'][j]=int(taObjectCity_reviews_output_places_restaurants['similarity'][j])
                    if(int(taObjectCity_reviews_output_places_restaurants['similarity'][j])==user_predict_attributes_restaurants_list[0]):
                       # print("yes")
                        X_places.append(taObjectCity_reviews_output_places_restaurants.taObject[j])
                    j+=1
                j=0
                for i in taObjectCity_reviews_output_places_restaurants.taObject:
                    #taObjectCity_reviews_output_places_restaurants['similarity'][j]=int(taObjectCity_reviews_output_places_restaurants['similarity'][j])
                    if(int(taObjectCity_reviews_output_places_restaurants['similarity'][j])!=user_predict_attributes_restaurants_list[0]):
                        #print("no")
                        X_places_other.append(taObjectCity_reviews_output_places_restaurants.taObject[j])
                    j+=1
                dic={}
                dic['places'] = X_places
                dic1={}
                dic1['places_other']=X_places_other
                if not dic:
                    if not dic1:
                        data = {"response": [ {"success":"0"} , {"message":"No places found"}] }
                        return json.dumps(data)
                else:    
                    places1={"response": [ {"success":"1"} ,{"message":"places fetched"}, {"places":dic}, {"places_other":dic1}] }
                    return json.dumps(places1)
            except:
                data = {"response": [ {"success":"0"} , {"message":"City Not in our database"}] }
                return json.dumps(data)
        else:
            data = {"response": [ {"success":"0"} , {"message":"No category of places provided"}] }
            return json.dumps(data)
    else:
        data = {"response": [ {"success":"0"} , {"message":"User not logged in"}] }
        return json.dumps(data)
################Suggest_Places#####################

###############Add Cities##########################
@app.route('/Addcities', methods=['GET', 'POST'])
def Addcities():
    if 'taObjectCity' in request.args:
        try:
            city = request.args.get('taObjectCity')
            #city="Mumbai (Bombay)"
            thr = Thread(target=AddCityWithScrapperAndTrainInBackground, args=[city])
            thr.start()
            cities_path = absoultepath+ "CityImages/"+city
            if(os.path.exists(cities_path)):
                data = {"response": [ {"success":"1"} , {"message":"City of "+city+" Already Exists for image Recognition. It might be in the training process. Please check after few days"}] }
                return json.dumps(data)
            else:
                data = {"response": [ {"success":"1"} , {"message":"City of "+city+" Will be Added, Return after a few days"}] }
                return json.dumps(data)
        except:
            data = {"response": [ {"success":"0"} , {"message":"Error!!! City of "+city+" Not Added"}] }
            return json.dumps(data)
    else:
        data = {"response": [ {"success":"0"} , {"message":"Error!!! City of "+city+" Not Added"}] }
        return json.dumps(data)

def AddCityWithScrapperAndTrainInBackground(city):
    try:
        scrappedcity=im.callscrapper(city)
        if(scrappedcity=="exist"):
            data = {"response": [ {"success":"1"} , {"message":"City of "+city+" Already Exists for image Recognition. It might be in the training process. Please check after few days"}] }
            return json.dumps(data)
        else:
            tsm.train_save_model(city)
            tsm.checkaccuracymodel(city)
            data = {"response": [ {"success":"1"} , {"message":"City of "+city+" Added"}] }
            return json.dumps(data)
    except:
        data = {"response": [ {"success":"0"} , {"message":"Error!!! City of "+city+" Not Added"}] }
        return json.dumps(data)
    
###############Add Cities##########################

################upload image#####################
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files['ionicfile']
            filename1=file.filename+".jpg"
            file.save(os.path.join("upload", filename1))
            data={"response": [ {"success":"1"} , {"message":"Picture Uploaded"}] }
            return json.dumps(data)
        except:
            data={"response": [ {"success":"0"} , {"message":"Picture not Uploaded"} ] }
            return json.dumps(data)
    else:
        data={"response": [ {"success":"0"} , {"message":"Picture could not be uploaded"}] }
        return json.dumps(data)
################upload image#####################

################find place#####################
@app.route('/Recognize', methods=['GET', 'POST'])
def Recognize():
    try:
        #import Images_TrainAndSaveModel as tsm1
        city = request.args.get('taObjectCity')
        #city="Mumbai (Bombay)"
        filename = request.args.get('filename')
        filename1=filename+".jpg"
        print(filename1)
        place=tsm.predictmodel(city,filename1)
        print(place)
        dic={}
        dic['place'] = place
        if(place=="exception"):
           data={"response": [ {"success":"0"} , {"message":"Place not Recognized"} ] }
           return json.dumps(data)
        else:
           data={"response": [ {"success":"1"} , {"message":"Place Found"}, {"place": place } ] }
           return json.dumps(data)
    except:
        data={"response": [ {"success":"0"} , {"message":"Error Recognizing Place"} ] }
        return json.dumps(data)
################find place#####################


if __name__=='__main__':
    app.run(host= '0.0.0.0',port=80,threaded=False)