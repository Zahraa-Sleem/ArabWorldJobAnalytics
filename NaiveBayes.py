import os
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')

# Define a function to tokenize and stem text
def tokenize_and_stem(text):
    tokens = nltk.word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return " ".join(stemmed_tokens)


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

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.1, random_state=42)

# Create a Porter Stemmer instance
stemmer = PorterStemmer()

# Apply the tokenization and stemming function to your job descriptions
X_train_stemmed = [tokenize_and_stem(desc) for desc in X_train]
X_test_stemmed = [tokenize_and_stem(desc) for desc in X_test]

# Create a CountVectorizer to convert the stemmed text data into numerical features
vectorizer = CountVectorizer(lowercase=True, stop_words='english')  # Add other preprocessing steps as needed
X_train_vec = vectorizer.fit_transform(X_train_stemmed)
X_test_vec = vectorizer.transform(X_test_stemmed)


clf = MultinomialNB()
clf.fit(X_train_vec, y_train)

accuracy = clf.score(X_test_vec, y_test)
print(f"Accuracy: {accuracy}")
train_accuracy = clf.score(X_train_vec, y_train)
print(f"Training Accuracy: {train_accuracy}")



