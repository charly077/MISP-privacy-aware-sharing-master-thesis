#######
# IOC #
#######
def get_types(ioc):
    return '||'.join(attr_type for attr_type in ioc)

def get_values(ioc):
    return '||'.join(ioc[attr_type] for attr_type in ioc)

def get_types_values(ioc):
    return (get_types(ioc), get_values(ioc))


#######
# AES #
#######
def aes_encrypt(key, nounce, message, attr_types):
    # Encrypt
    backend = default_backend()
    cipher = Cipher(algorithms.AES(dk), modes.CTR(nonce), backend=backend)
    encryptor = cipher.encryptor()
    ct_check = encryptor.update(b'\x00'*16)
    ct_message = encryptor.update(message.encode('utf-8'))
    ct_message += encryptor.finalize()

    # Create the rule
    rule = {}
    rule['salt'] = b64encode(salt).decode('ascii')
    rule['attributes'] = attr_types
    rule['nonce'] = b64encode(nonce).decode('ascii')
    rule['ciphertext-check'] = b64encode(ct_check).decode('ascii')
    rule['ciphertext'] = b64encode(ct_message).decode('ascii')

    return rule
