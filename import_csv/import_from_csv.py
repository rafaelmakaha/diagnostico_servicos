#!/usr/bin/python
# coding: utf-8
# This code uses the module available in https://github.com/axnsantana/python-limesurvey-rc
# under GPL-3.0 license

import pandas as pd
from pylimerc import PyLimeRc

if __name__ == "__main__":
    url = url
    username = username 
    password = password
    survey_id = survey_id

    df = pd.read_csv('/path/to/file.csv')
    
    main = PyLimeRc(url)
    main.get_session_key(username, password)

    for index, row in df.iterrows():
        print(row['organizacao'], row['nome_servico'])
        CA = row['organizacao']
        prov = row['nome_servico']
        data = {"startlanguage": "pt-BR", 
                "958979X2X3": CA, 
                "958979X2X4": prov, 
                }        
        result = main.add_response(survey_id, data)
        print result 