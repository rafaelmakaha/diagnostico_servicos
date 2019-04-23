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
#
#
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

import requests
from jsonpath_rw import jsonpath, parse
from data import data_minfra, data_novo52
# from mapping_me import columns_matrix, columns_simple, columns_categoric, columns_multiple, columns_other, \
#     columns_nomes
from mapping_minfra import columns_matrix, columns_simple, columns_categoric, columns_multiple, columns_other, \
    columns_nomes
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


def get_responses(url):
    headers = {
        "Authorization": "bearer %s" % "LBiQHvyhTbN3YqEM1ItHOhEpatfxh9QXkz6zsm2HSzeKLONgGF-WrEuWrXdf6T4YHlRjTiMjGnHZgnV1mQtLF2hEOdNtzTVW6xC9t7Qg8cpDF6ic7EroiVz-a4jsjb6e",
        "Content-Type": "application/json"
    }
    client = requests.session()
    response = client.get(url, headers=headers)
    return response.json()


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
            choices = None

        if choices:
            c['answer'] = ';'.join(choices)
        else:
            c['answer'] = None

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
            choice = None
        c['answer'] = choice
        question = recursive_find(questions, c['id'], 'id')['headings'][0]['heading']
        c['question'] = remove_html_tags(question)

        print('{0} - {1}: {2}'.format(count, c['column'], choice))
        count = count + 1

    print('multiple')
    columns_multiple_copy = columns_multiple.copy()
    for c in columns_multiple_copy:
        choice_subset = recursive_find(page, c['id'], 'id')
        if choice_subset:
            choice_subset = choice_subset['answers']
            choice_id = recursive_find(choice_subset, c['sub_id'], 'row_id')
            if choice_id:
                choice_id = choice_id['choice_id']
                choice = recursive_find(questions, choice_id, 'id')['text']
            else:
                choice = None
        else:
            choice = None

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
        if c['id']:
            answers = recursive_find(page, c['id'], 'id')
            if answers:
                answers = answers['answers']
                choice_id = find_row_col(answers, c['row_id'], c['col_id'])
                choice = recursive_find(questions, choice_id, 'id')
                if choice and 'text' in choice:
                    c['answer'] = choice['text']
                else:
                    c['answer'] = None
            else:
                c['answer'] = None
            question = recursive_find(questions, c['id'], 'id')['headings'][0]['heading']
            c['question'] = remove_html_tags(question)
            print('{0} - {1}: {2}'.format(count, c['column'], choice))
        else:
            c['answer'] = None

        count = count + 1

    columns_nomes_copy = columns_nomes.copy()
    if columns_nomes:
        print('columns_nomes')
        question_answers = recursive_find(page, columns_nomes_copy[0]['id'], 'id')['answers']
        choice0_id = recursive_find(question_answers, columns_nomes_copy[0]['col_id'], 'col_id')
        choice1_id = recursive_find(question_answers, columns_nomes_copy[1]['col_id'], 'col_id')

        if choice0_id:
            choice0 = recursive_find(questions, choice0_id['choice_id'], 'id')['text']
        else:
            choice0 = None

        if choice1_id:
            choice1 = recursive_find(questions, choice1_id['choice_id'], 'id')['text']
        else:
            choice1_id = recursive_find(question_answers, columns_nomes_copy[1]['other_id'], 'other_id')
            choice1 = choice1_id['text']

        if choice0_id or choice1_id:
            question = remove_html_tags(recursive_find(questions, columns_nomes_copy[0]['id'], 'id')['headings'][0]['heading'])
            columns_nomes_copy[0]['question'] = remove_html_tags(question)
            columns_nomes_copy[1]['question'] = remove_html_tags(question)
            columns_nomes_copy[2]['question'] = remove_html_tags(question)
        else:
            columns_nomes_copy[0]['question'] = None
            columns_nomes_copy[1]['question'] = None

        columns_nomes_copy[0]['answer'] = choice0
        columns_nomes_copy[1]['answer'] = choice1

        if 'row_id' in question_answers[0]:
            organizacao = remove_html_tags(recursive_find(questions, question_answers[0]['row_id'], 'id')['text'])
        else:
            organizacao = None

        columns_nomes_copy[2]['answer'] = organizacao

        print('{0} - {1}: {2}'.format(count, columns_nomes_copy[0]['column'], choice0))
        count = count + 1

        print('{0} - {1}: {2}'.format(count, columns_nomes_copy[1]['column'], choice1))
        count = count + 1

    result = columns_nomes_copy + columns_simple_copy + columns_categoric_copy + columns_multiple_copy + columns_other_copy + columns_matrix_copy
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
has_data = True
while has_data:
    for da in input['data']:
        page = da['pages']
        if da['response_status'] == 'partial':
            continue
        values, columns, questions_text = parse_answers(page, questions, ano)
        columns = ['id_resposta'] + columns
        if first:
            first = False
            ids = list(range(1, len(values) + 1))
            # dataset.append(questions_text)
            dataset.append(columns)
            # dataset.append(ids)

        values = [da['id']] + values
        dataset.append(values)

    if 'next' in input['links']:
        input = get_responses(input['links']['next'])
    else:
        has_data = False


with open('./dataset.csv', 'w') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
    wr.writerows(dataset)

