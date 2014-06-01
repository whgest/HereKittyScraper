# -*- coding: utf-8 -*-


BASE_URL = "http://www.petharbor.com/results.asp?"

SCRAPE_CATEGORIES = ['pet_id', 'gender', 'color', 'breed',
              'age_years', 'age_months', 'age_days', 'found_on', 'shelter_name']
DISCARDED_CATEGORIES = ['age_years', 'age_months', 'age_days']
SPECIAL_CATEGORIES = ['gender', 'pet_id', 'shelter_name', 'found_on', 'color']


def parse_ID(entry):
    if u"(" in entry:
        return [{"category": u"pet_id", "value": entry.split(u"(")[1].replace(u")", "")}, {"category": u"name", "value": entry.split(u"(")[0].replace(u" ", u"")}]
    else:
        return [{"category": u"pet_id", "value": entry}, {"category": "name", "value": u""}]

def parse_gender(entry):
    if u"(" in entry:
        return [{"category": u"gender", "value": entry.split(u"(")[0].replace(u" ", u"").lower()}, {"category": u"fixed", "value": 'true'}]
    else:
        return [{"category": u"gender", "value": entry.lower()}, {"category": u"fixed", "value": 'false'}]

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

def parse_color(entry):
    return [{"category": u"color", "value": entry.lower()}]

SPECIAL_FUNCTIONS = {
    "pet_id": parse_ID,
    "gender": parse_gender,
    "found_on": parse_foundon,
    "shelter_name": parse_shelter,
    "color": parse_color
}

PARAM_CONSTANTS = {
            "friends": "1",
            "samaritans": "1",
            "nosuccess": "0",
            "rows": "9999",
            "imght": "120",
            "imgres": "thumb",
            "shelterlist": ["%27ASTN%27"], #, "%27GRGT%27"],
            "page": "1",
            "view": "sysadm.v_animal",
            "orderby":"Brought%20To%20The%20Shelter"
}

QUERIES = [
    {"searchtype": "ADOPT", "atype": "other", "where": ["type_OTHER"]},
    {"searchtype": "LOST", "atype": "other", "where": ["type_OTHER"]},
    {"searchtype": "ADOPT", "atype": "cat", "where": ["type_CAT"]},
    {"searchtype": "ADOPT", "atype": "dog", "where": ["type_DOG"]},
    {"searchtype": "LOST", "atype": "cat", "where": ["type_CAT"]},
    {"searchtype": "LOST", "atype": "dog", "where": ["type_DOG"]}
]


class Query:
    def __init__(self, queries):
        self.queries = queries

    def query_list(self):
        query_list = []
        for query in self.queries:
            params = dict(query.items() + PARAM_CONSTANTS.items())
            query_list.append((self.generate_URL(params), query))
        print "QUERY LIST:", query_list
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