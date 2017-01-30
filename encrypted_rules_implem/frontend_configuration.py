# copy this file to configuration.py

class Configuration:
    # log
    log_path = '/var/log/squid3/access.log'

    # redis
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 1
    
    # misp
    misp_token = 'JNqWBxfPiIywz7hUe58MyJf6sD5PrTVaGm7hTn6c'

    # rules
    rule_location = 'rules'
