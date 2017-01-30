# Copy this file to configuration.py and complete the token
# centralize all configurations :

class Configuration:
    # log
    log_path = '/var/log/squid3/access.log'

    # redis
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    
    # misp
    misp_token = 'JNqWBxfPiIywz7hUe58MyJf6sD5PrTVaGm7hTn6c'
    misp_email = 'admin@misp.training '

    # misp Web Api
    misp_url = 'https://192.168.30.20/'

    # misp mysql database
    user = 'charles'
    password = 'Password1234'
    host = '192.168.30.20'
    dbname = 'misp'
    
    # useful lists
    alexa = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/alexa/list.json'
    tlds = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/tlds/list.json'
    second_domain = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/second-level-tlds/list.json'
    empty_hash = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/empty-hashes/list.json'
    google = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/google/list.json'
    ip_multicast = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/multicast/list.json'
    public_dns_v4 = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/public-dns-v4/list.json'
    public_dns_v6 = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/public-dns-v6/list.json'
    ip_rfc1918 = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/rfc1918/list.json'
    ip_rfc5737 = 'https://raw.githubusercontent.com/MISP/misp-warninglists/master/lists/rfc5735/list.json'

