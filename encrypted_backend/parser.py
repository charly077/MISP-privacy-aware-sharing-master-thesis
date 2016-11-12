import json
import redis as r


def read_json(name):
    with open('res/{}.json'.format(name), 'r') as f:
        json_list = json.load(f)
    return json_list['list']


class Parser(object):
    """
        parse data:
            -> check if not in the lists
            -> lower case
    """

    def __init__(self):
        self.fp_url_list = read_json('alexa')
        self.fp_url_domain_list = read_json('tlds')
        self.fp_url_domain_list.extend(read_json('second_domain'))
        self.fp_hash_list = read_json('empty_hash')
        self.fp_google_list = read_json('google')
        self.fp_ip_list = read_json('ip_multicast')
        self.fp_ip_list.extend(read_json('ip_rfc1918'))
        self.fp_ip_list.extend(read_json('ip_rfc5737'))
        self.fp_ip_list.extend(read_json('public_dns_v4'))
        self.fp_ip_list.extend(read_json('public_dns_v6'))
        self.fp_ad_list = read_json('ad')

    def add_p(p, value, event_dico):
        # hash data
        hash_value = SHA256.new(value.strip().lower()).hexdigest()
        # create course of action
        coa = event_dico["event_id"] 
        coa = coa + : + event_dico["uuid"]
        coa = coa + : + event_dico["data"]
        coa = coa + : + event_dico["category"]
        coa = coa + : + event_dico["type"]
        coa = coa + : + event_dico["value"]
        # TODO encrypt data as explained in the article + 
        # add to redis pipeline
        r.sadd(value, coa)

    def url(self, event_dico, redis_p):
        if event_dico["type"] != "url":
            add_p(event_dico['value'], event_dico)

        # parse the value
        val = get_val_list(['url','uri', 'link'], event_dico)
        
        #TODO parse the value !!! get back the code from augustus :)

    def domain(self, event_dico, redis_p):
        # TODO
        pass

    def ip(self, event_dico, redis_p):
        # TODO
        pass

    def email(self, event_dico, redis_p):
        # TODO
        pass

def get_val(type, event_dico):
    split_type = event_dico["type"].split('|')
    val = ""
    for i in range(len(split_type)):
        if split_type[i] == type:
            val = event_dico["value"].split('|')[i]
    return val

def get_val_list(list, event_dico):
    val = ""
    for elem in list:
        if elem in event_dico["type"]:
            val = get_val(elem, event_dico)
    return val
