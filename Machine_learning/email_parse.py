from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import numpy as np
import string
import re
from time import time
def remove_unwanted(line):

    ignore_list = ['Message-ID:', 'Date:', 'From:', 'To:', 'Cc:', 'Bcc:', 'Subject:', 'Mime-Version:',
                   'Sent:', 'Content-Type:', 'Content-Transfer-Encoding:', 'X-', '\n', '[',
                   ' << O', 'cc:', ' -----O', '-----O', 'Facsimile:', 'Phone:', '----', ' ---',
                   'Tel' 'Fax', 'Forwarded by', '@', 'CC:', 'BCC:', 'bcc:', 'E-Mail:', 'E:', 'Email:']
    invalid_chars = list(string.punctuation)
    invalid_chars.extend(['\n', '\t'])
    names = [name.lower().split() for name in data_dict.keys()]

    phone_regex = re.compile(r'^(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
    time_regex = re.compile(r'\d{1,2}(?:(?:am|pm)|(?::\d{1,2})(?:am|pm)?)')
    date_regex = re.compile(r'\d+/\d+/\d{4}')
    if line.strip(' ').startswith(tuple(ignore_list)):
        return ''
    else:
        if line.startswith('\t') and '@' in line:
            return ''
        else:
            remove_from_line = []
            line = phone_regex.sub('', line)
            line = time_regex.sub('', line)
            line = date_regex.sub('', line)
            precheck_remove = ['.com', '.net', '.org', 'http', 'www', '@', 'cc:']
            for item in line.split(' '):
                for check in precheck_remove:
                    if item.find(check) != -1:
                        item = item.translate(None, ''.join(invalid_chars))
                        remove_from_line.append(item.lower())
                        break
            valid_line = ''.join(char for char in line if char not in invalid_chars).lower()
            if not valid_line.isspace():
                valid_line = valid_line.split(' ')
            else:
                return ''

            for item in valid_line:
                count = 0
                if unicode(item).isnumeric():
                    remove_from_line.append(item)
                    continue
                for name in names:
                    if len(name) < 4:
                        if item == name[0] or item == name[1]:
                            remove_from_line.append(item)
                    elif len(name) < 6:
                        if item == name[0] or item == name[2]:
                            remove_from_line.append(item)
                    else:
                        continue
                if item.find('http') != -1 or item.find('https') != -1 or item.find('www') != -1 or item.find('.com') != -1:
                    remove_from_line.append(item)
                    continue
                for char in item:
                    if unicode(char).isdigit():
                        count += 1
                if count >= 1:
                    remove_from_line.append(item)
                    continue
                if item.find('cc') != -1:
                    remove_from_line.append(item)
                if item.find('dear') != -1:
                    remove_from_line.append(item)
                if item.find('thank') != -1:
                    remove_from_line.append(item)
                if item.find('pmr') != -1:
                    remove_from_line.append(item)
                if item.find('pm') != -1:
                    remove_from_line.append(item)
                if len(item) == 1:
                    remove_from_line.append(item)
                if item == '':
                    remove_from_line.append(item)

            email_line = [word for word in valid_line if word not in remove_from_line]
            if email_line != [] and email_line[0] != '':
                return ' '.join(email_line)+ ' '
            else:
                return ''


def email_parse(data_dict):
    tfidf_dict = {}
    tfidf = TfidfVectorizer(analyzer='word', stop_words='english')

    for person in data_dict:
        t0 = time()

        if data_dict[person]['email_address'] != "NaN":
            tfidf_dict[person] = {}
            tfidf_dict[person]['poi'] = data_dict[person]['poi']
            from_emails = []
            to_emails = []

    # Try to open email list,  if fail from_emails is an empty list
            try:
                from_list = open('emails_by_address/from_' + data_dict[person]['email_address'] + '.txt')
                count = 0
            except:
                from_emails = []
            if from_list is not None:
                for em_line in from_list:
                    file_nm = em_line.strip('\n')
    # Try to open the next email found in the email list, if fail move to the next one
                    try:
                        email_file = open(file_nm)
                    except:
                        continue
                    email = ''
                    for line in email_file:
                        email += remove_unwanted(line)
                    from_emails.append(email)
                    email_file.close()

                from_list.close()
                from_list = None
            try:
                to_list = open('emails_by_address/to_' + data_dict[person]['email_address'] + '.txt')
                count = 0
            except:
                to_emails = []
            if to_list is not None:
                for em_line in to_list:
                    file_nm = em_line.strip('\n')
                    try:
                        email_file = open(file_nm)
                    except:
                        continue
                    email = ''
                    for line in email_file:
                       email += remove_unwanted(line)

                    to_emails.append(email)
                    email_file.close()
                    email = None

                to_list.close()
                to_list = None

    # creates a TFIDF list to do a feature selection step on to choose the most effective word features
            if to_emails != [] and from_emails != []:
                emails = from_emails
                emails.extend(to_emails)
                del from_emails
                del to_emails
                doc = tfidf.fit_transform(emails)
                emails = None
                feature_names = tfidf.get_feature_names()
                phrase_scores = []
                for i in range(0, doc.shape[0]):
                    dense = doc.getrow(i).todense().tolist()[0]
                    phrase_scores.extend([pair for pair in zip(range(0, len(dense)), dense) if pair[1] > 0])

                dense = None
                doc = None

                for i in range(0, len(phrase_scores)):
                        if not unicode(feature_names[phrase_scores[i][0]]).isnumeric():
                            tfidf_dict[person][feature_names[phrase_scores[i][0]]] = phrase_scores[i][1]
                print(person)
                print str(((float(len(tfidf_dict)) / 84.0)*100)) + "% complete"
                print("Done in %0.3fs" % (time() - t0))
            else:
                tfidf_dict.pop(person, None)


    # print statement because the run time is long and I wanted to make sure that the program did not hang.


    # Dumping the resultant dictionary to a pickle file so that I don't have to run this code again
    pickle.dump(tfidf_dict, open('tfidf_data.pkl', 'wb'), 2)


def email_data_finalize():
    data_file = open('tfidf_data.pkl', 'rb')
    tfidf_dict = pickle.load(data_file)
    data_file.close()
    list_of_features = []

    for key in tfidf_dict.keys():
        list_of_features.extend(tfidf_dict[key].keys())
    # removes duplicates by casting as a set then back to a list
    list_of_features = list(set(list_of_features))
    list_of_features.sort()
    features_to_remove = []

    # inserts 'poi' to the front of the list
    list_of_features.insert(0, 'poi')
    i = 1
    # Finds a list of features that are not in an individual entry, and adds them
    for key in tfidf_dict:
        features_in_dict = tfidf_dict[key].keys()
        features_to_remove = [x for x in features_in_dict if x not in list_of_features]
        tfidf_dict[key] = {feat: tfidf_dict[key][feat] for feat in tfidf_dict[key] if feat not in features_to_remove}
        diff = list(set(list_of_features) - set(tfidf_dict[key].keys()))
        for item in diff:
            tfidf_dict[key][item] = 0.0
        print str(i) + " out of " + str(len(tfidf_dict))
        i += 1

    # Dump email data and list of features so that I don't have to run this section of code again
    pickle.dump(tfidf_dict, open('email_data.pkl', 'wb'), 2)
    pickle.dump(list_of_features, open('list_of_features.pkl', 'wb'), 2)