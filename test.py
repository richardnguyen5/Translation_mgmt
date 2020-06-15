import os
import re 
import pandas as pd
from os import listdir
from os.path import isfile, join, isdir

#targeted column headers to read into dataframe   
all_survey          = pd.DataFrame()   #read excel "survey" sheeet column headers into DF
all_choices         = pd.DataFrame()   #read excel "survey" sheeet column headers into DF
choices_headers_all = pd.DataFrame()

header_label            = ['name','label'] 
header_hint             = ['name','hint']
header_constrain        = ['name','constraint_message']
choices_header_label    = ['list_name','name','label'] 

# def read_foldername()
########################################################
#returns list of all folders in directory 
########################################################
mypath = os.getcwd() 
only_folders = [f for f in listdir(mypath) if isdir(join(mypath, f))]

#folders need to be 4 characters with the first 2 for country code, last 2 for round/phase
data  = [] 
survey, phase, choices =  'survey','phase', 'choices'
for num, each in enumerate(only_folders, start=0):
    data.append([each[0:2], each[2:4]])
only_folders_data = pd.DataFrame(columns =[survey,phase], data = data)

# def read_xlsfiles()
########################################################
#returns list of all files in each folders  
########################################################
all_files = [] 
for num, folder in enumerate (only_folders, start = 0):
    files_path = mypath + '/' + folder
    only_files = [f for f in listdir(files_path) if isfile(join(files_path, f))]
    # all_files += only_files

    for f in only_files:
        file_path = files_path + '/' + f
        #TODO:create function for this 
        survey_headers = pd.read_excel(file_path, sheet_name = survey, nrows=0)
        header_label_match = [] 
        header_hint_match = [] 
        header_constrain_match  = [] 
        #match column headers to only extract label, hint, constrain  
        #TODO:create function for this  
        for header in survey_headers: 
            for each in header_label:
                if re.match(each, header):
                    header_label_match.append(header)   
                else:
                    pass
            for each in header_hint:
                if re.match(each, header):
                    header_hint_match.append(header)   
                else:
                    pass
            for each in header_constrain:
                if re.match(each, header):
                    header_constrain_match.append(header)   
                else:
                    pass

        #same process for choice sheet 
        choices_headers = pd.read_excel(file_path, sheet_name = choices, nrows=0)
        choices_header_label_match = [] 
        choices_header_hint_match = [] 
        choices_header_constrain_match  = [] 
        #match column headers to only extract list_name, name, languages from choices_sheet   
        #TODO:create function for this  
        for header in choices_headers: 
            for each in choices_header_label:
                if re.match(each, header):
                    choices_header_label_match.append(header)   
                else:
                    pass


        #create 3 dataframes for labels, hints, and constrains msg
        #remove blank rows, and rename column headers for merging purpose
        #TODO:create function for this#
        survey_labels = pd.read_excel(file_path, sheet_name = survey ,usecols=header_label_match)
        survey_labels = survey_labels.dropna(how='any',axis=0)
        languages = []

        for each in survey_labels.columns:
            languages.append(each.split(':')[-1])

        survey_labels.columns  = languages
        survey_hints = pd.read_excel(file_path, sheet_name = survey,usecols=header_hint_match)
        survey_hints = survey_hints.dropna(how='any',axis=0)
        languages = []
        for each in survey_hints.columns:
            languages.append(each.split(':')[-1])


        survey_hints.columns  = languages
        survey_constrains = pd.read_excel(file_path, sheet_name = survey,usecols=header_constrain_match)
        survey_constrains = survey_constrains.dropna(how='any',axis=0)
        languages = []
        for each in survey_constrains.columns:
            languages.append(each.split(':')[-1])

        survey_constrains.columns  = languages

        #create 1 DF for choices 
        choices_labels = pd.read_excel(file_path, sheet_name = choices ,usecols=choices_header_label_match)
        choices_labels = choices_labels.dropna(how='any',axis=0)
        languages = []

        for each in choices_labels.columns:
            languages.append(each.split(':')[-1])

        choices_labels.columns  = languages

        #append all DF translation together
        survey_sheet = survey_labels.append(survey_hints).append(survey_constrains).append(choices_labels)
        all_survey = all_survey.append(survey_sheet)
        



all_survey.to_excel("text.xlsx", index = False)



# #append all DF file info + translation together 
# for each in survey_sheet.columns:
#     if each == survey:
#         survey_sheet[each] = (file_info.iloc[0,0]) #survey is 1 value 
#     elif each == phase:
#         survey_sheet[each] = (file_info.iloc[0,1]) #phase is 2nd value
#     else:
#         pass

##TODO: only delete N/A rows where "name" column is N/A
# survey_sheet = survey_sheet.dropna(how='any',axis=0)
