# -*- coding: utf-8 -*-


BASE_URL = "http://www.petharbor.com/results.asp?"

SCRAPE_CATEGORIES = ['pet_id', 'gender', 'color', 'breed',
              'age_years', 'age_months', 'age_days', 'found_on', 'shelter_name']
DISCARDED_CATEGORIES = ['age_years', 'age_months', 'age_days']
SPECIAL_CATEGORIES = ['gender', 'pet_id', 'shelter_name', 'found_on']

def parse_ID(entry):
    if u"(" in entry:
        return [{"category": u"pet_id", "value": entry.split(u"(")[1].replace(u")", "")}, {"category": u"name", "value": entry.split(u"(")[0].replace(u" ", u"")}]
    else:
        return [{"category": u"pet_id", "value": entry}, {"category": "name", "value": u""}]

def parse_gender(entry):
    if u"(" in entry:
        return [{"category": u"gender", "value": entry.split(u"(")[0].replace(u" ", u"")}, {"category": u"fixed", "value": 'true'}]
    else:
        return [{"category": u"gender", "value": entry}, {"category": u"fixed", "value": 'false'}]

def parse_foundon(entry):
    if u"Reported On " in entry:
        return [{"category": u"found_on", "value": entry.split(u"Reported On ")[1].replace(".", "-")}]
    else:
        return [{"category": u"found_on", "value": entry.replace(".", "-")}]

def parse_shelter(entry):
    if u"Reported To " in entry:
        return [{"category": u"shelter_name", "value": entry.split(u"Reported To ")[1]}]
    else:
        return [{"category": u"shelter_name", "value": entry}]


SPECIAL_FUNCTIONS = {
    "pet_id": parse_ID,
    "gender": parse_gender,
    "found_on": parse_foundon,
    "shelter_name": parse_shelter
}


#only "atype", "where", "searchtype" values (and possibly "shelterlist") should ever change, AFAIK
DEFAULT_PARAMS = {
            #"searchtype": "ADOPT",
            "friends": "1",
            "samaritans": "1",
            "nosuccess": "0",
            "rows": "9999",
            "imght": "120",
            "imgres": "thumb",
            "shelterlist": ["%27ASTN%27"], #, "%27GRGT%27"],
            #"atype": "cat",
            "page": "1",
            #"where": ["type_CAT"],
            "view": "sysadm.v_animal",
            "orderby":"Brought%20To%20The%20Shelter"
}

QUERIES = [
    {"searchtype": "ADOPT", "atype": "cat", "where": ["type_CAT"]},
    {"searchtype": "ADOPT", "atype": "dog", "where": ["type_DOG"]},
    {"searchtype": "ADOPT", "atype": "other", "where": ["type_OTHER"]},
    {"searchtype": "LOST", "atype": "cat", "where": ["type_CAT"]},
    {"searchtype": "LOST", "atype": "dog", "where": ["type_DOG"]},
    {"searchtype": "LOST", "atype": "other", "where": ["type_OTHER"]},
]


class Query:
    def __init__(self, queries):
        self.queries = queries

    def query_list(self):
        query_list = []
        for query in self.queries:
            params = dict(query.items() + DEFAULT_PARAMS.items())
            query_list.append((self.generate_URL(params), query))
        return query_list

    def generate_URL(self, parameters):
        request = BASE_URL
        for param in parameters:
            if type(parameters[param]) is str:
                request += "%s=%s&" % (param, parameters[param])
            elif type(parameters[param]) is list:
                q_list = parameters[param]
                request += param + "="
                for q in q_list:
                    request += "%s," % q
                #remove trailing comma
                request = request[:-1]
                request += "&"
        request = request[:-1]
        return request

QUERY = Query(QUERIES)


def post_pets():
    pass

# update
# reconcile