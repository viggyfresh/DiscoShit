import csv
import numpy as np
import voting
import demographic
from sklearn import svm
from sklearn.cluster import KMeans


counties = ["Alameda", "Butte" , "Contra Costa", "El Dorado", "Fresno",
"Humboldt", "Imperial", "Kern", "Kings", "Lake", "Los Angeles", "Madera",
"Marin", "Mendocino", "Merced", "Monterey", "Napa", "Nevada", "Orange",
"Placer", "Riverside", "Sacramento", "San Bernardino", "San Diego",
"San Francisco", "San Joaquin", "San Luis Obispo", "San Mateo",
"Santa Barbara", "Santa Clara", "Santa Cruz", "Shasta", "Solano", "Sonoma",
"Stanislaus", "Sutter", "Tulare", "Ventura", "Yolo", "Yuba"]

# sample_issues = [{ "year": 2006, "prop": "1A", "polarity": "Yes" }, { "year": 2008, "prop": "12", "polarity": "No" }]
# sample_tag = { "name": "DiscoShit", "type": "Percent", "demographics": [10, 11, 12] }





def compose_design_matrix(issue, tag):
    designMatrix = None
    targetMatrix = None

    for county in counties:
        feature_vec, target_vec = demographic.construct_submatrix(issue["year"], tag["demographics"], county, issue["prop"], tag["type"], issue["polarity"])
        if designMatrix is None:
            designMatrix = feature_vec
        else:
            designMatrix = np.vstack((designMatrix, feature_vec))
        if targetMatrix is None:
            targetMatrix = target_vec
        else:
            targetMatrix = np.vstack((targetMatrix, target_vec))

    return designMatrix, targetMatrix

def combine_design_matrices(issues, tag):
    designMatrix = None
    targetMatrix = None

    for issue in issues:
        temp_design, temp_target = compose_design_matrix(issue, tag)
        if designMatrix is None:
            designMatrix = temp_design
        else:
            designMatrix = np.vstack((designMatrix, temp_design))
        if targetMatrix is None:
            targetMatrix = temp_target
        else:
            targetMatrix = np.vstack((targetMatrix, temp_target))

    # print designMatrix
    # print targetMatrix
    return designMatrix, targetMatrix


def zero_or_one(number):
    if number > 50:
        return 1
    else:
        return 0

def convert_to_binary_target(targetMatrix):
    vecfunc = np.vectorize(zero_or_one)
    return vecfunc(targetMatrix)


def build_classifier_model(issues, tag):
    design_matrix, target_matrix = combine_design_matrices(issues, tag)
    binary_target_matrix = convert_to_binary_target(target_matrix)
    clf = svm.LinearSVC()
    clf.fit(design_matrix, np.asarray(binary_target_matrix).ravel().transpose())
    return clf, design_matrix, binary_target_matrix



def test_classifier_model(model, design_matrix, target_matrix):
    num_errors = 0.0
    target_array = np.asarray(target_matrix).ravel()
    for i in range(len(target_array) - 1):
        if model.predict(design_matrix[i])[0] != np.array(target_array[i]):
            num_errors += 1
    print "Number of errors:"
    print num_errors
    print "Error percentage:"
    print num_errors / len(target_array)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_all_training_issues():

    issues = []

    f = open('Proposition Labels.csv', 'rU')
    for line in f:
        issue_array = line.split(',')
        if issue_array[0] != '2014' and is_number(issue_array[0]):
            issue_dict = {'year': issue_array[0], 'prop': issue_array[4], 'polarity': 'Yes'}
            issues.append(issue_dict)
    return issues



def test():
    sample_issues = [{ "year": 2008, "prop": "11", "polarity": "No" }]
    sample_tag = { "name": "DiscoShit", "type": "Percent", "demographics": [26] }
    model, design_matrix, target_matrix = build_classifier_model(sample_issues, sample_tag)
    test_classifier_model(model, design_matrix, target_matrix.ravel())



test()


# combine_design_matrices(sample_issues, sample_tag)
