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
# HOST = "https://api.surveymonkey.net"
# # SURVEY_LIST_ENDPOINT = '/v3/surveys/166556535/responses/10564608343'
# # SURVEY_LIST_ENDPOINT = '/v3//surveys/166556535/pages'
# SURVEY_LIST_ENDPOINT = '/v3/surveys/166556535/details'
# # SURVEY_LIST_ENDPOINT = "/v3/surveys/166556535/responses/bulk"
# # SURVEY_LIST_ENDPOINT = '/v3/surveys/166556535/responses/10579548780/details'
#
#
#
# uri = "%s%s" % (HOST, SURVEY_LIST_ENDPOINT)
#
# # response = client.post(uri, headers=headers, data=json.dumps(data))
# response = client.get(uri, headers=headers)
# response_json = response.json()
# #survey_list = response_json["data"]["surveys"]
#
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
#
# print(response_json)

from data import data_test
from .jpath import jpath

d = data_test
print(jpath.get_dict_value(d, "data/pages/questions"))
