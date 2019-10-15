import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.metrics import confusion_matrix


# Create a dictionary of words with its frequency
def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    all_words = []
    for mail in emails:
        with open(mail) as m:
            for i, line in enumerate(m):
                if i == 2:  # Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words

    dictionary = Counter(all_words)
    list_to_remove = list(dictionary)
    for item in list_to_remove:
        # if item.isalpha() == False:
        #     del dictionary[item]
        # el
        if len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(100)
    # Paste code for non-word removal here(code snippet is given below)
    return dictionary


def extract_features(mail_dir):
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.ones((len(files),100))
    docID = 0
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


train_dir = 'train-mails'
dictionary = make_Dictionary(train_dir)


# Prepare feature vectors per training mail and its labels


class_identifier = np.zeros(702)
class_identifier[351:702] = 1
train_matrix = extract_features(train_dir)


#total_num_occurance = np.sum(train_matrix, axis = 0)
ham_num_occurance = np.sum(train_matrix[0:351], axis = 0)
spam_num_occurance = np.sum(train_matrix[351:702], axis = 0)
process = lambda x: np.log(x/(451))
spam_frequency = process(spam_num_occurance)
ham_frequency = process(ham_num_occurance)

spam_dictionary = {}
ham_dictionary = {}

for iter, freq in enumerate(dictionary):
    spam_dictionary[freq[0]] = spam_frequency[iter]
    ham_dictionary[freq[0]] = ham_frequency[iter]

print(ham_frequency)
print(ham_dictionary)
print(spam_frequency)
print(spam_dictionary)

# # Training Naive bayes classifier
#
# model1 = MultinomialNB()
# model1.fit(train_matrix, class_identifier)
# # model2.fit(train_matrix, class_identifier)
#
# # Test the unseen mails for Spam
# test_dir = 'test-mails'
# test_matrix = extract_features(test_dir)
# test_labels = np.zeros(260)
# test_labels[130:260] = 1
# result1 = model1.predict(test_matrix)
# # result2 = model2.predict(test_matrix)
# print(confusion_matrix(test_labels, result1))
# # print(confusion_matrix(test_labels, result2))
