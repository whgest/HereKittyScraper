__author__ = 'wgest'

import requests
import json
import urllib2


def update_pets():
    fin = open('../spider_data.json')
    url = 'http://pure-retreat-7270.herokuapp.com/populator/update'
    headers = {'content-type': 'application/json'}
    #payload = "{\"pets\":{\"0\":" + fin.read().replace("[", "").replace("]", "") + "}}"
    payload = fin.read().replace("[", "").replace("]", "")
    new_payload = ""
    for i, entry in enumerate(payload.split("}")):
        res = entry.replace("{", "\"%s\":{" % str(i)) + "}"
        new_payload += res

    new_payload = "{\"pets\":{" + new_payload + "}"
    print new_payload
    response = requests.post(url, data=new_payload, headers=headers)
    print response

def reconcile_pets():
    url = 'http://pure-retreat-7270.herokuapp.com/populator/reconcile'
    fin = open('../spider_data.json')
    headers = {'content-type': 'application/json'}
    all_pets = json.load(fin)
    all_ids = []
    for pet in all_pets:
        all_ids.append(pet["pet_id"])

    new_payload = ""
    for i, entry in enumerate(all_ids):
        new_payload += "\"%s\":\"%s\"," % (str(i), entry)
    new_payload = new_payload[:-1]
    new_payload = "{\"pet_ids\":{" + new_payload + "}}"

    print new_payload
    response = requests.post(url, data=new_payload, headers=headers)
    print response

def main():
    update_pets()
    reconcile_pets()

if __name__ == "main":
    main()