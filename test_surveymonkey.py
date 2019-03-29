# import requests
# import json
#
# client = requests.session()
#
# headers = {
#     "Authorization": "bearer %s" % "LBiQHvyhTbN3YqEM1ItHOhEpatfxh9QXkz6zsm2HSzeKLONgGF-WrEuWrXdf6T4YHlRjTiMjGnHZgnV1mQtLF2hEOdNtzTVW6xC9t7Qg8cpDF6ic7EroiVz-a4jsjb6e",
#     "Content-Type": "application/json"
# }
#
# data = {}
#
# HOST = "https://api.surveymonkey.net" #MINFRA 166556535   #ME 168829664
# # SURVEY_LIST_ENDPOINT = '/v3/surveys/166556535/responses/10564608343'
# # SURVEY_LIST_ENDPOINT = '/v3/surveys/166556535/pages'
# # SURVEY_LIST_ENDPOINT = '/v3/surveys/166556535/details'
# SURVEY_LIST_ENDPOINT = "/v3/surveys/166556535/responses/bulk"
# # SURVEY_LIST_ENDPOINT = '/v3/surveys/166556535/responses/10579548780/details'
#
# ''
#
# uri = "%s%s" % (HOST, SURVEY_LIST_ENDPOINT)
#
# # response = client.post(uri, headers=headers, data=json.dumps(data))
# response = client.get(uri, headers=headers)
# response_json = response.json()
# #survey_list = response_json["data"]["surveys"]
#
# print(response_json)
# print(response_json)


# import requests
# import json
#
# client = requests.session()
#
# headers = {
# "Authorization": "bearer %s" % "LBiQHvyhTbN3YqEM1ItHOhEpatfxh9QXkz6zsm2HSzeKLONgGF-WrEuWrXdf6T4YHlRjTiMjGnHZgnV1mQtLF2hEOdNtzTVW6xC9t7Qg8cpDF6ic7EroiVz-a4jsjb6e",
# "Content-Type": "application/json"
# }
#
# data = {}
#
# HOST = "https://api.surveymonkey.net"
# SURVEY_LIST_ENDPOINT = "/v3/surveys"
#
# uri = "%s%s" % (HOST, SURVEY_LIST_ENDPOINT)
#
# response = client.get(uri, headers=headers)
#
# response_json = response.json()
# #survey_list = response_json["data"]["surveys"]
# print(response_json)
# print(response_json)
import csv

from jsonpath_rw import jsonpath, parse
from data import data_minfra, data_novo52
from mapping_me import columns_matrix, columns_simple, columns_categoric, columns_multiple, columns_other
from questions import question_me52, question_minfra


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_choices(l):
    choices = []
    for i in l:
        choices.append(i['choice_id'])


def recursive_find(d, value, key):
    if isinstance(d, dict):
        for k, v in d.items():
            if k == key and v == value:
                return d
            if isinstance(v, dict):
                ret = recursive_find(v, value, key)
                if ret:
                    return ret
            elif isinstance(v, list):
                for el in v:
                    ret = recursive_find(el, value, key)
                    if ret:
                        return ret
    elif isinstance(d, list):
        for el in d:
            ret = recursive_find(el, value, key)
            if ret:
                return ret
    return None


def find_row_col(l, row, col):
    for i in l:
        if i['row_id'] == row and i['col_id'] == col:
            return i['choice_id']
    return None


def parse_answers(page, questions, ano):
    count = 1
    columns_categoric_copy = columns_categoric.copy()
    print('categoric')

    for c in columns_categoric_copy:
        choices_id = recursive_find(page, c['id'], 'id')
        choices = []

        if choices_id:
            choices_id = choices_id['answers'] #[0]['choice_id']

            for i in choices_id:
                if 'choice_id' in i:
                    choice = recursive_find(questions, i['choice_id'], 'id')['text']
                    choices.append(remove_html_tags(choice))
        else:
            choices.append('')

        c['answer'] = ';'.join(choices)
        question = recursive_find(questions, c['id'], 'id')['headings'][0]['heading']
        c['question'] = remove_html_tags(question)

        print('{0} - {1}: {2}'.format(count, c['column'], choice))
        count = count + 1

    print('simple')
    columns_simple_copy = columns_simple.copy()
    for c in columns_simple_copy:
        choice = recursive_find(page, c['id'], 'id')
        if choice:
            choice = choice['answers'][0]['text']
        else:
            choice = ''
        c['answer'] = choice
        question = recursive_find(questions, c['id'], 'id')['headings'][0]['heading']
        c['question'] = remove_html_tags(question)

        print('{0} - {1}: {2}'.format(count, c['column'], choice))
        count = count + 1

    print('multiple')
    columns_multiple_copy = columns_multiple.copy()
    for c in columns_multiple_copy:
        choice_subset = recursive_find(page, c['id'], 'id')['answers']
        choice_id = recursive_find(choice_subset, c['sub_id'], 'row_id')
        if choice_id:
            choice_id = choice_id['choice_id']
            choice = recursive_find(questions, choice_id, 'id')['text']
        else:
            choice = ''
        c['answer'] = choice
        question = recursive_find(questions, c['id'], 'id')['headings'][0]['heading']
        c['question'] = remove_html_tags(question)

        print('{0} - {1}: {2}'.format(count, c['column'], choice))
        count = count + 1

    print('other')
    columns_other_copy = columns_other.copy()
    for c in columns_other_copy:
        choice = recursive_find(page, c['id'], 'other_id')
        if choice and 'text' in choice:
            c['answer'] = choice['text']
            print('{0} - {1}: {2}'.format(count, c['column'], choice['text']))
        else:
            c['answer'] = None
            print('{0} - {1}: {2}'.format(count, c['column'], choice))

        c['question'] = c['column']
        count = count + 1

    print('matrix')
    columns_matrix_copy = columns_matrix.copy()
    for c in columns_matrix_copy:
        answers = recursive_find(page, c['id'], 'id')['answers']
        choice_id = find_row_col(answers, c['row_id'], c['col_id'])
        choice = recursive_find(questions, choice_id, 'id')
        if choice and 'text' in choice:
            c['answer'] = choice['text']
        else:
            c['answer'] = None
        question = recursive_find(questions, c['id'], 'id')['headings'][0]['heading']
        c['question'] = remove_html_tags(question)

        print('{0} - {1}: {2}'.format(count, c['column'], choice))
        count = count + 1

    result = columns_simple_copy + columns_categoric_copy + columns_multiple_copy + columns_other_copy + columns_matrix_copy
    values = [ano] + [d['answer'] for d in result]
    columns = ['ano'] + [d['column'] for d in result]
    questions_text = ['ano'] + [d['question'] for d in result]
    print('{0} {1} {2}'.format(len(values), len(columns), len(questions_text)))

    simple_cols = [{'question': d['question'], 'column': d['column'], 'id': d['id']} for d in columns_simple_copy]
    print('columns_simple = {0}'.format(simple_cols))

    categ_cols = [{'question': d['question'], 'column': d['column'], 'id': d['id']} for d in columns_categoric_copy]
    print('columns_categoric = {0}'.format(categ_cols))

    multiple_cols = [{'question': d['question'], 'column': d['column'], 'id': d['id']} for d in columns_multiple_copy]
    print('columns_multiple = {0}'.format(multiple_cols))

    other_cols = [{'question': d['question'], 'column': d['column'], 'id': d['id']} for d in columns_other_copy]
    print('columns_other = {0}'.format(other_cols))

    matrix_cols = [{'question': d['question'], 'column': d['column'], 'id': d['id']} for d in columns_matrix_copy]
    print('columns_matrix = {0}'.format(matrix_cols))

    return values, columns, questions_text


jsonpath_expr = parse('data[*].pages')
question_expr = parse('pages[*].questions')
questions = [match.value for match in question_expr.find(question_minfra)]
dataset = []
first = True

input = data_minfra
ano = input['data'][0]['date_modified'].split('-')[0]

for match in jsonpath_expr.find(input):
    page = match.value
    values, columns, questions_text = parse_answers(page, questions, ano)
    if first:
        first = False
        dataset.append(questions_text)
        dataset.append(columns)

    dataset.append(values)

with open('./dataset.csv', 'w') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerows(dataset)

