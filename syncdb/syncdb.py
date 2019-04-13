import itertools
import requests
from connect_database import ConnectDatabase

def get_orgaos(input):
    result = {}
    for i in input:
        servico_id = i['id'].split('/')[6]
        servico_nome = i['nome']
        orgao_id = i['orgao']['id'].split('/')[5]
        orgao_nome = i['orgao']['nomeOrgao']
        if orgao_id in result:
            result[orgao_id].append({'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_nome': '{0}'.format(orgao_nome,),
                                     'orgao_id': orgao_id.zfill(8)})
        else:
            result[orgao_id] = [{'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_nome': '{0}'.format(orgao_nome),
                                 'orgao_id': orgao_id.zfill(8)}]

    return result


def get_dataset(orgaos):
    orgaos_output = {}
    servicos_output = {}

    for o in orgaos:
        orgaos_output.update({
            '{0}'.format(orgaos[o][0]['orgao_id']):'{0}'.format(orgaos[o][0]['orgao_nome'].replace('&lt;', '<').replace('&gt;', '>')),
        })

        for s in orgaos[o]:
            servicos_output.update({
                '{0}{1}'.format(s['orgao_id'], s['servico_id']):'{0}'.format(s['servico_nome'].replace('&lt;', '<').replace('&gt;', '>')),
            })

    return orgaos_output, servicos_output

if __name__ == '__main__':
    # Run once every 24 hours
    while True:
        try:
            # Url for the serv.
            url = 'https://www.servicos.gov.br/api/v1/servicos/'

            # Variables used to insert into db
            language = 'pt-BR'
            qid_orgao = qid1  # replace with the question id
            qid_servico = qid2 # replace with the question id

            response = requests.get(url)

            # Use API and get the serv. and org. and return dict
            orgaos_set = get_orgaos(response.json()['resposta'])
            orgaos_set, servicos_set = get_dataset(orgaos_set)

            # Connect to db and get tuples with current answer 
            orgaos_db_tp = ConnectDatabase.queryAnswer(qid_orgao)
            servicos_db_tp = ConnectDatabase.queryAnswer(qid_servico)

            # Convert tuples to dict
            orgaos_db = dict((y, x) for x, y in orgaos_db_tp)
            servicos_db = dict((y, x) for x, y in servicos_db_tp)
            
            # The variables are used to in the sort of the table
            i = len(orgaos_db)
            j = len(servicos_db)
            
            # Compare the db with api and insert the difference
            unmatched_orgao = set(orgaos_set.keys()) - set(orgaos_db.keys())
            for code in unmatched_orgao: 
                ConnectDatabase.insertAnswer(qid_orgao, code, orgaos_set[code], (i+1), 0, language, 0)
                i = i+1
                print(code)

            # Compare the db with api and insert the difference
            unmatched_servico = set(servicos_set.keys()) - set(servicos_db.keys())
            for code in unmatched_servico:
                ConnectDatabase.insertAnswer(qid_servico, code, servicos_set[code], (j+1), 0, language, 0)
                j=j+1
                print(code) 
        except:
            print("Error will try again next day")
        
        time.sleep(86400) # set sleep time here 86400s == 24h
    