key_blacklist = [
    '__file__', 'app', 'router', 'name_index',
    'directory_handler', 'directory_view', 'os', 'path', 'pardir', '_static_folder',
    '__loader__', '0',  '1', '3', '4', '5', '6', '7', '8', '9',
]

value_blacklist = [
    'ls', 'dir', 'nl', 'nc', 'cat', 'tail', 'more', 'flag', 'cut', 'awk',
    'strings', 'od', 'ping', 'sort', 'ch', 'zip', 'mod', 'sl', 'find',
    'sed', 'cp', 'mv', 'ty', 'grep', 'fd', 'df', 'sudo', 'more', 'cc', 'tac', 'less',
    'head', '{', '}', 'tar', 'zip', 'gcc', 'uniq', 'vi', 'vim', 'file', 'xxd',
    'base64', 'date', 'env', '?', 'wget', '"', 'id', 'whoami', 'readflag'
]

# 将黑名单转换为字节串
key_blacklist_bytes = [word.encode() for word in key_blacklist]
value_blacklist_bytes = [word.encode() for word in value_blacklist]

def check_blacklist(data, blacklist):
    for item in blacklist:
        if item in data:
            return False
    return True

def pwaf(key):
    # 将 key 转换为字节串
    key_bytes = key.encode()
    if not check_blacklist(key_bytes, key_blacklist_bytes):
        print(f"Key contains blacklisted words.")
        return False
    return True

def cwaf(value):
    if len(value) > 77:
        print("Value exceeds 77 characters.")
        return False
    
    # 将 value 转换为字节串
    value_bytes = value.encode()
    if not check_blacklist(value_bytes, value_blacklist_bytes):
        print(f"Value contains blacklisted words.")
        return False
    return True

