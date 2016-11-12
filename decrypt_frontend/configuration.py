# centralize all configurations :

class Configuration:
    # log
    log_path = '/var/log/squid3/access.log'

    # redis
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    
    # misp
    misp_token = 'rQEKsHU9KQAvXLcqLniqd0DWbPnu8dDA3hlwZfFJ'

    # rules
    rule_location = 'rules'
