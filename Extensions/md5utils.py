import md5

def getMD5HexDigest(inputString):
    return md5.new(inputString).hexdigest()