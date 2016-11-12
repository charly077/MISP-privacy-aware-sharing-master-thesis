# centralize all configurations :

class Configuration:
    # log
    log_path = '/var/log/squid3/access.log'

    # redis
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0
    
    # misp
    misp_token = 'misp token'
