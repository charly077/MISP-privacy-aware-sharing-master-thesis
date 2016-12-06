#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import Configuration
import requests
import json
import os, shutil

conf = Configuration()

# update false positive list : https://github.com/MISP/misp-warninglists
# and get updated values
def save_json(url, name, remove_point=False, add_www=False):
    req = requests.get(url)
    l = req.json()['list']
    l = [val.lower() for val in l]
    if remove_point:
        list2 = [val[1:] for val in l if val.startswith('.')]
        list2.extend([val for val in l if not val.startswith('.')])
        l = list2
    if add_www:
        list2 = ['www.%s' % val for val in l]
        l.extend(list2)
    json_list = {'list': l}
    with open('res/{}.json'.format(name), 'w+') as f:
        json.dump(json_list, f)

    
def update():
    # first let clean the ressources
    if os.path.exists("res"):
        shutil.rmtree("res")
    os.mkdir("res")
    
    """
    ************** not used for now *******************
    # List of the top level domains
    save_json(conf.tlds, 'tlds')

    # list of the most visited web pages (alexa) with www. added
    save_json(conf.alexa, 'alexa', add_www=True)

    # list of empty hashes
    save_json(conf.empty_hash, 'empty_hash')

    # list of google domains (without the firs .)
    save_json(conf.google, 'google', remove_point=True)

    # list of ip multicast
    save_json(conf.ip_multicast, 'ip_multicast')

    # list of public dns
    save_json(conf.public_dns_v4, 'public_dns_v4')
    save_json(conf.public_dns_v6, 'public_dns_v6')

    # lists of usual internal network ip
    save_json(conf.ip_rfc1918, 'ip_rfc1918')
    save_json(conf.ip_rfc5737, 'ip_rfc5737')

    # list of second level domains
    save_json(conf.second_domain, 'second_domain')

    # get ad_domain to avoid
    ad_req = requests.get("https://pgl.yoyo.org/as/serverlist.php?showintro=0;hostformat=hosts")
    ad_lines = ad_req.text.split('\n')
    ad_lines = [line for line in ad_lines if line.startswith("127")]
    ad_list = [line.split(" ")[1] for line in ad_lines]

    ad_json = {'list': ad_list, 'name': 'advertisement domains', 'version': 0,
               'description': 'This list comes from https://pgl.yoyo.org/as/serverlist.php?showintro=0;hostformat=hosts',
               'matching_attributes': ["hostname", "domain", "domain|ip"]}
    with open('res/ad.json', 'w+') as f:
        json.dump(ad_json, f)


    """

    # get misp data in csv
    session = requests.Session()
    session.verify = True
    session.proxies = None

    header = {}
    header['Authorization'] = conf.misp_token
    session.headers.update(header)

    # Change to csv (only download ids elements!)
    events = session.get('{}events/csv/download/'.format(conf.misp_url))

    with open('res/misp_events.csv', 'w') as f:
        f.write(events.text)

if __name__ == "__main__":
    update()
