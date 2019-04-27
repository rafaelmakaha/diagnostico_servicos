import itertools
import dicttoxml
import requests
import declxml as xml
import json
from pprint import pprint


def generate_codes(l, n):
    yield from itertools.product(*([l] * n))


def write_file(name, data):
    text_file = open(name, "w")
    text_file.write(data)
    text_file.close()


def get_serivcos_orgaos(input):
    result = []
    for i in input:
        servico_id = i['id'].split('/')[6]
        servico_nome = i['nome']
        orgao_id = i['orgao']['id'].split('/')[5]
        orgao_nome = i['orgao']['nomeOrgao']
        result.append(
            {'servico_id': servico_id, 'servico_nome': '{0}'.format(servico_nome), 'orgao_id': orgao_id, 'orgao_nome': '{0}'.format(orgao_nome)})

    return result


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


def create_codes(orgaos, qid_orgao, qid_serv, language):
    count_orgao = 1
    count_serv = 1
    orgaos_output = {'rows': []}
    servicos_output = {'rows': []}

    for o in orgaos:
        orgaos_output['rows'].append({
            'qid': "<![CDATA[{0}]]>".format(qid_orgao),
            'code': "<![CDATA[{0}]]>".format(orgaos[o][0]['orgao_id']),
            'answer': "<![CDATA[{0}]]>".format(orgaos[o][0]['orgao_nome']),
            'sortorder': "<![CDATA[{0}]]>".format(count_orgao),
            'language': "<![CDATA[{0}]]>".format(language),
            'assessment_value': "<![CDATA[0]]>",
            'scale_id': "<![CDATA[0]]>"
        })
        count_orgao = count_orgao + 1

        for s in orgaos[o]:
            servicos_output['rows'].append({
                'qid': "<![CDATA[{0}]]>".format(qid_serv),
                'code': "<![CDATA[{0}{1}]]>".format(s['orgao_id'], s['servico_id']),
                'answer': "<![CDATA[{0}]]>".format(s['servico_nome']),
                'sortorder': "<![CDATA[{0}]]>".format(count_serv),
                'language': "<![CDATA[{0}]]>".format(language),
                'assessment_value': "<![CDATA[0]]>",
                'scale_id': "<![CDATA[0]]>"
            })
            count_serv = count_serv + 1

    return orgaos_output, servicos_output


def json2cdata(input):
    author_processor = xml.dictionary('rows', [
        xml.array(xml.dictionary('row', [
            xml.string('qid'),
            xml.integer('code'),
            xml.string('answer'),
            xml.integer('sortorder'),
            xml.integer('assessment_value'),
            xml.integer('language'),
            xml.integer('scale_id'),
        ]), alias='rows')
    ])
    xmlstr = xml.serialize_to_string(author_processor, input, indent='   ')
    return xmlstr




url = 'https://www.servicos.gov.br/api/v1/servicos/'
response = requests.get(url)
orgaos_set = get_orgaos(response.json()['resposta'])
dataset_orgaos, dataset_servicos = create_codes(orgaos_set, 3, 186, 'pt-BR')

with open('servicos.json', 'w') as fp:
    json.dump(orgaos_set,fp)

# xml_orgaos = json2cdata(dataset_orgaos)
# xml_servicos = json2cdata(dataset_servicos)
# write_file('xml_servicos', xml_servicos.replace('&lt;', '<').replace('&gt;', '>'))
# write_file('xml_orgaos', xml_orgaos.replace('&lt;', '<').replace('&gt;', '>'))
