BASE_URL = "http://www.petharbor.com/results.asp?"


class Query:
    def __init__(self, params):
        self.parameters = params

    def generate_URL(self):
        request = BASE_URL
        for param in self.parameters:
            if type(self.parameters[param]) is str:
                request += "%s=%s&" % (param, self.parameters[param])
            elif type(self.parameters[param]) is list:
                q_list = self.parameters[param]
                request += param + "="
                for q in q_list:
                    request += "%s," % q
                #remove trailing comma
                request = request[:-1]
                request += "&"
        request = request[:-1]
        return request

PARAMS = {
            "searchtype": "LOST",
            "friends": "1",
            "samaritans": "1",
            "nosuccess": "0",
            "rows": "9999",
            "imght": "120",
            "imgres": "thumb",
            "shelterlist": ["%27ASTN%27", "%27GRGT%27"],
            "atype": "cat",
            "page": "1",
            "where": ["type_CAT", "gender_f"],
            "view": "sysadm.v_animal"
}




QUERY = Query(PARAMS)
