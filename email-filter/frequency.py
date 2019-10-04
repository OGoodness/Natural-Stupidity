# import re
# import string
import glob, os
from collections import Counter

#
# frequency = {}
# os.chdir("train-mails")
# for file in glob.glob("*.txt"):
#     with open(file, 'r') as f:
#         for line in f:
#             for word in line.split():
#                 count = frequency.get(word, 0)
#                 frequency[word] = count + 1
#
#
#
# frequency= sorted(frequency.items(), key = lambda x : x[1])[::-1]
#

# print(frequency)
import os, string
import numpy as np
from collections import Counter

def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    all_words = []
    for mail in emails:
        with open(mail) as m:
            for i, line in enumerate(m):
                if i == 2:  # Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words

    return Counter(all_words)

def extract_features(mail_dir):
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1
    return features_matrix

# Create a dictionary of words with its frequency

train_dir = 'train-mails'
dictionary = make_Dictionary(train_dir)

list_to_remove = list(dictionary)
for item in list_to_remove:
    # if item.isalpha() == False and item not in string.punctuation:
    #     print(item)
    #     del dictionary[item]
    # el
    if len(item) == 1:
        del dictionary[item]
dictionary = dictionary.most_common(3000)

# Prepare feature vectors per training mail and its labels

train_labels = np.zeros(702)
train_labels[351:701] = 1
train_matrix = extract_features(train_dir)
print(train_labels, train_matrix)
print(dictionary)

# # Training SVM and Naive bayes classifier
#
# model1 = MultinomialNB()
# model2 = LinearSVC()
# model1.fit(train_matrix, train_labels)
# model2.fit(train_matrix, train_labels)
#
# # Test the unseen mails for Spam
# test_dir = 'test-mails'
# test_matrix = extract_features(test_dir)
# test_labels = np.zeros(260)
# test_labels[130:260] = 1
# result1 = model1.predict(test_matrix)
# result2 = model2.predict(test_matrix)
# print(confusion_matrix(test_labels, result1))
# print(confusion_matrix(test_labels, result2))

