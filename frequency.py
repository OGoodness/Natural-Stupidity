import math
from os import listdir
from collections import defaultdict, OrderedDict
import re
from collections import Counter

# get list of all training mail files
spam_dictionary = defaultdict(int)
global_dictionary = defaultdict(int)
ham_dictionary = defaultdict(int)
feature_matrix = {}
train_spam_count = 0
train_ham_count = 0
train_dir = 'train-mails/'
files = listdir(train_dir)

#This deals with 3 dictionaries.
#   Global dictionary: Global dictionary to keep track of all words
#   Regular dictionary: Dictionary passed in that needs to get added to (spam/ham)
#   Email dictionary: Returned so it can be added to dictionary of files
def emailDictionary(email, dictionary):
    email_dictionary = defaultdict(int)
    for line in email:
        for word in line.split():
            if word.isalpha() is True and len(word) >= 5:
                email_dictionary[word] +=1
                dictionary[word] += 1
                global_dictionary[word] +=1
    return email_dictionary



#Builds dictionary for spam and ham seperately. While at the same time making the feature matrix
for file in files:
    email_name = train_dir + file
    # open file
    with open(email_name, 'r') as email:
        #Check if current file is Spam/Ham
        if 'spm' in file:
            # Track # of Spam files
            train_spam_count +=1
            feature_matrix.update(({file: emailDictionary(email, spam_dictionary)}))
        else:
            #Track # of Ham files
            train_ham_count +=1
            feature_matrix.update(({file: emailDictionary(email, ham_dictionary)}))

#Sort the dictionary and then get top 3000 words (returns list)
sorted_spam =sorted(spam_dictionary.items(), key=lambda item: item[1], reverse=True)[:3000]
sorted_ham = sorted(ham_dictionary.items(), key=lambda item: item[1], reverse=True)[:3000]

#Reinitialize dictionary to clear values
ham_dictionary, spam_dictionary = {}, {}
#Turn list into dictionary
for item in sorted_ham:
    ham_dictionary.update({item[0]: item[1]})
for item in sorted_spam:
    spam_dictionary.update({item[0]: item[1]})
print(spam_dictionary)


print(feature_matrix)


spam_decision = {}
#Final Result Variables
total_spam = 0
total_ham = 0
a = 1
for file in files:
    ham = 0
    spam = 0
    with open(train_dir + file, 'r') as email:
        for line in email:
            for word in line.split():
                if word.isalpha() is True and len(word) >= 4:

                    feature_count = 0 if feature_matrix.get(file).get(word) is None else feature_matrix.get(file).get(word)
                    ham_count = ham_dictionary.get(word) if ham_dictionary.get(word) is not None else 0
                    spam_count = spam_dictionary.get(word) if spam_dictionary.get(word) is not None else 0

                    p_of_evidience_given_spam = (spam_count + a) / (train_spam_count + feature_count * a)
                    p_of_features_in_spam = train_spam_count / (train_spam_count + train_ham_count)
                    spam += math.log(p_of_evidience_given_spam + a, math.e) * (feature_count + a) + math.log(p_of_features_in_spam + a, math.e)

                    p_of_evidience_given_ham = (ham_count + a) / (train_ham_count + feature_count * a)
                    p_of_features_in_ham = train_ham_count / (train_spam_count + train_ham_count)
                    ham += math.log(p_of_evidience_given_ham + a, math.e) * (feature_count + a) + math.log(p_of_features_in_ham + a, math.e)

    if(spam > ham):
        spam_decision.update({file: 'spam' + str(spam)})
        total_spam +=1
    else:
        spam_decision.update({file: 'ham' + str(ham)})
        total_ham +=1


print("Spam: " + str(total_spam) + " Ham: " + str(total_ham))
print("Spam: " + str((total_spam+total_ham)/2 /total_spam ) + " Ham: " + str(total_ham / ((total_ham + total_spam)/2)))
