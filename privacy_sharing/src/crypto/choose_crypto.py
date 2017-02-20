def Crypto(name, conf):
    if (name == 'pbkdf2'):
        from crypto.pbkdf2 import Pbkdf2
        return Pbkdf2(conf)
