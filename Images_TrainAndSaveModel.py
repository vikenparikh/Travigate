# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 03:06:17 2018
@author: Viken
"""
# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
from keras.preprocessing import image

absoultepath= "/home/ubuntu/Travigate/"

def train_save_model(city):
    subfolders = [f.name for f in os.scandir(absoultepath+'CityImages/'+city+'/train') if f.is_dir() ]
    numofclasses=len(subfolders)
    
    # Initialising the CNN
    classifier = Sequential()
    # Step 1 - Convolution
    classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
    # Step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    # Adding a second convolutional layer
    classifier.add(Conv2D(64, (3, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    # Step 3 - Flattening
    classifier.add(Flatten())
    # Step 4 - Full connection
    classifier.add(Dense(units = 128, activation = 'relu'))
    classifier.add(Dense(units = numofclasses, activation = 'softmax'))#units=number of classes to classify
    # Compiling the CNN
    classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
    
    # Part 2 - Fitting the CNN to the images
    train_datagen = ImageDataGenerator(rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True)
    test_datagen = ImageDataGenerator(rescale = 1./255)
    training_set = train_datagen.flow_from_directory(absoultepath+'CityImages/'+city+'/train',target_size=(64,64),batch_size=32,class_mode='categorical')
    test_set = test_datagen.flow_from_directory(absoultepath+'CityImages/'+city+'/train',target_size = (64, 64),batch_size = 32,class_mode = 'categorical')
    classifier.fit_generator(training_set,steps_per_epoch = 50,epochs = 100,validation_data = test_set,validation_steps = 200)
    #validation steps=2000,epochs=25,steps_per_epoch=8000
    # Part 3 - Making new predictions
    
    #save model
    model_json=classifier.to_json()
    
    with open((city+" "+"model.json"),"w") as json_file:
        json_file.write(model_json)    
    classifier.save_weights((city+" "+"classifier.h5"))
    
def checkaccuracymodel(city):
    #CheckAccuracy
    subfolders = [f.name for f in os.scandir(absoultepath+'CityImages/'+city+'/train') if f.is_dir() ]
    numofclasses=len(subfolders)
    json_file = open((city+" "+"model.json"),'r')
    loaded_model_json=json_file.read()
    json_file.close
    loaded_model=model_from_json(loaded_model_json)
    loaded_model.load_weights((city+" "+"classifier.h5"))
    loaded_model.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])
    train_datagen = ImageDataGenerator(rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True)
    test_datagen = ImageDataGenerator(rescale = 1./255)
    training_set = train_datagen.flow_from_directory(absoultepath+'CityImages/'+city+'/train',target_size=(64,64),batch_size=32,class_mode='categorical')
    
    total=0
    count=0
    countincorrect=0
    j=0
    while j<numofclasses:
        i=1
        counttemp=0
        totaltemp=0
        countincorrecttemp=0
        while i<100:
            try:
                total=total+1
                totaltemp=totaltemp+1
                path=absoultepath+'CityImages/'+city+'/train/'+subfolders[j]+'/'+str(object=i)+subfolders[j]+'.jpg'
                test_image = image.load_img(path, target_size = (64, 64))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis = 0)
                result = loaded_model.predict(test_image)
                res=result.tolist()
                finalresult=res[0].index(1.)
                answer=training_set.class_indices
                for places,output_class in answer.items():
                    if output_class == finalresult:
                        place = places
                        if(subfolders[j]==place):
                            count=count+1
                            counttemp=counttemp+1
            except:
                countincorrect=countincorrect+1
                countincorrecttemp=countincorrecttemp+1
            i=i+1
        accuracy=(counttemp/totaltemp)*100
        print(subfolders[j] +" Accuracy = " + str(round(accuracy, 2)))
        j=j+1
    accuracy=(count/total)*100
    print("Final Average Accuracy of "+ str(object=j) +" places = "+str(round(accuracy, 2)))
    
def predictmodel(city,imagename):
    #city="Mumbai (Bombay)"
    #imagename="Vikenupload1.jpg"
    subfolders = [f.name for f in os.scandir(absoultepath+'CityImages/'+city+'/train') if f.is_dir() ]
    numofclasses=len(subfolders)
    '''
    json_file = open((city+" "+"model.json"),'r')
    print("Yes1")
    loaded_model_json=json_file.read()
    json_file.close
    print("Yes9")
    loaded_model=model_from_json(loaded_model_json)
    print("Yes9")
    loaded_model.load_weights((city+" "+"classifier.h5"))
    loaded_model.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])
    '''
    train_datagen = ImageDataGenerator(rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True)
    #print("Yes9")
    training_set = train_datagen.flow_from_directory(absoultepath+'CityImages/'+city+'/train',target_size=(64,64),batch_size=32,class_mode='categorical')
    try:
        path=absoultepath+'static/upload/'+imagename
        json_file = open((city+" "+"model.json"),'r')
        loaded_model_json=json_file.read()
        json_file.close
        #print("Yes0")
        try:
            loaded_model=model_from_json(loaded_model_json)
            loaded_model.load_weights((city+" "+"classifier.h5"))
        except:
            print("2nd Image Exception, Restart console")    
        loaded_model.compile(optimizer = 'adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])
        test_image = image.load_img(path, target_size = (64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = loaded_model.predict(test_image)
        #print("Yes1")
        res=result.tolist()
        train_datagen = ImageDataGenerator(rescale = 1./255,
        shear_range = 0.2,
        zoom_range = 0.2,
        horizontal_flip = True)
        training_set = train_datagen.flow_from_directory(absoultepath+'CityImages/'+city+'/train',target_size=(64,64),batch_size=32,class_mode='categorical')
        finalresult=res[0].index(1.)
        answer=training_set.class_indices
        #print("Yes2")
        for places,output_class in answer.items():
            if output_class == finalresult:
                place = places
                print(place)
                return place
    except:
        return ("exception")
'''
if __name__=='__main__':
    city="Mumbai (Bombay)"
    imagename="Vikenupload1.jpg"
    train_save_model(city)
    checkaccuracymodel(city)
    predictmodel(city,imagename)
'''