
import requests
import json

def update_pets():
    fin = open('../spider_data.json')
    url = 'http://pure-retreat-7270.herokuapp.com/populator/update'
    headers = {'content-type': 'application/json'}
    pets_dict = {}
    index_dict = {}
    pets = json.load(fin)
    for i, pet in enumerate(pets):
        index_dict[str(i)] = pet
    pets_dict["pets"] = index_dict
    print json.dumps(pets_dict)
    response = requests.post(url, data=json.dumps(pets_dict), headers=headers)
    print response

def reconcile_pets():
    url = 'http://pure-retreat-7270.herokuapp.com/populator/reconcile'
    fin = open('../spider_data.json')
    headers = {'content-type': 'application/json'}
    all_pets = json.load(fin)
    all_ids = []
    for pet in all_pets:
        all_ids.append(pet["pet_id"])

    ids_dict = {}
    index_dict = {}
    for i, id in enumerate(all_ids):
        index_dict[str(i)] = id
    ids_dict["pet_ids"] = index_dict
    print json.dumps(ids_dict)
    response = requests.post(url, data=json.dumps(ids_dict), headers=headers)
    print response

def erase_db():
    url = 'http://pure-retreat-7270.herokuapp.com/populator/reconcile'
    headers = {'content-type': 'application/json'}

    ids_dict = {}
    index_dict = {}

    ids_dict["pet_ids"] = index_dict
    print json.dumps(ids_dict)
    response = requests.post(url, data=json.dumps(ids_dict), headers=headers)
    print response

def main():
    update_pets()
    reconcile_pets()
    #erase_db()

if __name__ == "__main__":
    main()