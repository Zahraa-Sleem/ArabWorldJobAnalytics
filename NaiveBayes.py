import os
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split


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

filtered_data = [entry for entry in data if entry.get("Job Title") != "Unspecified"]

# Separate features (job descriptions) and labels (job titles)
X = [entry["Description"] for entry in filtered_data]
y = [entry["Job Title"] for entry in filtered_data]

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

clf = MultinomialNB()
clf.fit(X_train_vec, y_train)

accuracy = clf.score(X_test_vec, y_test)
print(f"Accuracy: {accuracy}")



