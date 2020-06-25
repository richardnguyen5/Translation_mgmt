import os
import re 
import pandas as pd
from os import listdir
from os.path import isfile, join, isdir

output_df               = pd.DataFrame()   
header_label            = ['name','label'] 
header_hint             = ['name','hint']
header_constrain        = ['name','constraint_message']
choices_header_label    = ['list_name','name','label'] 
survey, phase, choices,sheet,settings,form_id  =  'survey','phase', 'choices', 'sheet', 'settings', 'form_id'
header_label_match = [] 
header_hint_match = [] 
header_constrain_match  = [] 
choices_header_label_match = [] 

def main()
#returns list of all folders in current directory 
    mypath = os.getcwd() 
    only_folders = [f for f in listdir(mypath) if isdir(join(mypath, f))]

    #returns list of all files in each directory
    for loop_one, folder in enumerate (only_folders, start = 0):
        files_path = mypath + '/' + folder
        only_files = [f for f in listdir(files_path) if isfile(join(files_path, f))]

        #read each file
        for loop_two, f in enumerate(only_files, start = 0):
            file_path = files_path + '/' + f
            #only reads column header of survey sheet to extract target data 
            survey_headers = pd.read_excel(file_path, sheet_name = survey, nrows=0)
            #match column headers to target label, hint, constrain  
            for header in survey_headers: 
                header_label_match.append(header_match(header, header_label))
                header_hint_match.append(header_match(header, header_hint))
                header_constrain_match.append(header_match(header, header_constrain))

            #same process as above for choices sheet except we don't need hints or contraints 
            choices_headers = pd.read_excel(file_path, sheet_name = choices, nrows=0)
            for header in choices_headers:
                choices_header_label_match.append(header_match(header, choices_headers))

            # 3 DFs for labels, hints, and constrains in survey sheet / #1 DF for labels in choices sheet
            survey_labels       = read_rename_target_columns(file_path, survey, header_label_match)
            survey_hints        = read_rename_target_columns(file_path, survey, header_hint_match)
            survey_constrains   = read_rename_target_columns(file_path, survey, header_constrain_match)
            choices_labels      = read_rename_target_columns(file_path, choices, choices_header_label_match)

            #1 DF for settings sheet 1st row to capture and split the form_id column 
            settings_df = pd.read_excel(file_path, sheet_name = settings, nrows=1)
            
            #checks 'form_id' column even exists to prevent error when it's not in the excel file
            #split form_id string to get 2 letter form_id (CQ,FQ,HQ...) 
            for each in settings_df.columns:
                if re.match(form_id, each):
                    settings_form_id = settings_df.loc[0,each].split('-')[0]
                    break 
                else:
                    #default form_id when files were missing that column
                    settings_form_id = "no form_id"

            #Append 3 DFs from survey sheet into 1   
            survey_sheet = survey_labels.append(survey_hints).append(survey_constrains)
            
            #add 'sheet' column and set value to 'survey' or 'choices'
            survey_sheet.insert(column = sheet, loc= 0, value = survey)
            choices_labels.insert(column = sheet, loc= 0, value = choices)

            #Append 'choices' DF to rest of 'survey' DF
            survey_sheet = survey_sheet.append(choices_labels)
            
            #add columns to DF from folder and file information:
            #   Assumption:
            #   first 2 characters of folder name is the country code (BF, NI, etc..)
            #   rest of of folder name is Phase, Round, or special rounds like Nutrition, Abortion   
            #   file_data and file_info lists must match in length 
            file_info = ["File Name", "Country", "Phase", "FormID"]
            file_data = [f, folder[0:2], folder[2:], settings_form_id] 
            for num in range(len(file_info)):
                survey_sheet.insert(column = file_info[num], loc= 0, value = 'NA')
                survey_sheet[file_info[num]] = file_data[num]
            
            #Append ALL DF
            output_df = output_df.append(survey_sheet)
            
    output_df.to_excel("translation.xlsx", index = False)

#return column header name when match with header_label  
def header_match(header, header_label):
    for each in header_label:
        if re.match(each, header):
        return each 
    else:
        pass

# remove blank rows, and rename column headers for merging purpose with other DFs
def read_rename_target_columns(file_path, sheet_name, target_headers):
    data = pd.read_excel(file_path, sheet_name = sheet_name ,usecols=target_headers)
    data = data.dropna(how='any',axis=0)
    languages = []
    for each in data.columns:
    	languages.append(each.split(':')[-1])
    data.columns = languages
    return data

if __name__ == "__main__":
    main()