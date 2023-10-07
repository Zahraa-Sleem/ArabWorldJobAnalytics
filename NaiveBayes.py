import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
import category_encoders as ce
from sklearn.preprocessing import RobustScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

def make_data_set(folder_name):
    directory_path = folder_name

    all_files_and_directories = os.listdir(directory_path)
    
    data=[]
    
    for file in all_files_and_directories:
            try:
                with open(folder_name+"/"+file, "r") as json_file:
                    all=json.load(json_file)
                    info={"Job Title":all["Data"]["Job Role"],"Description":all["Description"]}
                    data.append(info) 
            except: 
                pass
    
    return data

data=make_data_set("data_store")

Training_testing=[entry for entry in data if entry["Job Title"] != "Unspecified"]

df = pd.DataFrame(Training_testing)

X = df['Description']

y = df['Job Title']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

encoder = ce.OneHotEncoder(cols=['Description'])

X_train = encoder.fit_transform(X_train)

X_test = encoder.transform(X_test)

cols = X_train.columns

scaler = RobustScaler()

X_train = scaler.fit_transform(X_train)

X_test = scaler.transform(X_test)

X_train = pd.DataFrame(X_train, columns=[cols])

X_test = pd.DataFrame(X_test, columns=[cols])

gnb = GaussianNB()

gnb.fit(X_train, y_train)

y_pred = gnb.predict(X_test)

print('Model accuracy score: {0:0.4f}'. format(accuracy_score(y_test, y_pred)))

y_pred_train = gnb.predict(X_train)

print('Training-set accuracy score: {0:0.4f}'. format(accuracy_score(y_train, y_pred_train)))

# print the scores on training and test set

print('Training set score: {:.4f}'.format(gnb.score(X_train, y_train)))

print('Test set score: {:.4f}'.format(gnb.score(X_test, y_test)))