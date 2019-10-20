import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.metrics import confusion_matrix


# Create a dictionary of words with its frequency
def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    all_words = []
    count = 0
    for mail in emails:
        with open(mail) as m:
            for i, line in enumerate(m):
                if i == 2:
                    words = line.split()
                    all_words += words

    dictionary = Counter(all_words)
    list_to_remove = list(dictionary)
    for item in list_to_remove:
        if item == "Subject:":
            del dictionary[item]
        if len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(SIZE)
    # Paste code for non-word removal here(code snippet is given below)
    return dictionary


def extract_features(mail_dir):
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.ones((len(files), SIZE))
    docID = 0
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
            words = line.split()
            if i == 2:
                for word in words:
                  wordID = 0
                  for i,d in enumerate(dictionary):
                    if d[0] == word:
                      wordID = i
                      features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1
    return features_matrix

def test_data(test_dir, spam_count, ham_count, spam_dict, ham_dict):
    files = [os.path.join(test_dir, fi) for fi in os.listdir(test_dir)]
    file_index = 0
    is_spam = []
    spam = 0
    ham = 0
    for fil in files:
        with open(fil) as fi:
            for i, line in enumerate(fi):
                words = line.split()
                for word in words:
                    if word in spam_dict and word in train_matrix:
                        spam = spam + spam_dict[word] * train_matrix[word] + np.log(1.0 / 2.0)
                        ham = ham + ham_dict[word] * train_matrix[word] + np.log(1.0 / 2.0)
                    else:
                        spam = spam + (1/(351 + 3000)) + np.log(1.0 / 2.0)
                        ham = ham + (1/(351 + 3000)) + np.log(1.0 / 2.0)
            if spam > ham:
                is_spam += [True]
            else:
                is_spam += [False]
            file_index += 1
    return is_spam

SIZE = 3000
train_dir = 'train-mails'
small_test = 'small-test'
test_mails = 'test-mails'
dictionary = make_Dictionary(train_dir)
test = dict(dictionary)

# Prepare feature vectors per training mail and its labels


class_identifier = np.zeros(SIZE)
class_identifier[352:702] = 1
train_matrix = extract_features(train_dir)


#total_num_occurance = np.sum(train_matrix, axis = 0)
ham_num_occurance = np.sum(train_matrix[0:351], axis = 0)
spam_num_occurance = np.sum(train_matrix[352:702], axis = 0)
process = lambda x: np.log((x/(351 + 3000)))
spam_frequency = process(spam_num_occurance)
ham_frequency = process(ham_num_occurance)

spam_dictionary = {}
ham_dictionary = {}

for iter, freq in enumerate(dictionary):
    spam_dictionary[freq[0]] = spam_frequency[iter]
    ham_dictionary[freq[0]] = ham_frequency[iter]

#print(ham_frequency)
#print(ham_dictionary)
#print(spam_frequency)
#print(spam_dictionary)
#results = finalCalculations(small_test)

is_spam = test_data(test_mails, 130, 130, spam_dictionary, ham_dictionary)

ham = 0
spam = 0
for value in is_spam:
    if value == True:
        spam += 1
    else:
        ham += 1

print(spam)
print(ham)
print("Accuracy: " + str((260-abs(spam-ham))/260))
print(is_spam.count)



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