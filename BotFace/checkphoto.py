def Read(img):
    try:
        with open(img, 'rb') as f:
            return f.read()
    except IOError:
        return False


def Write(name, data):

    try:
        with open(name, 'wb') as f:
            f.write(data)
    except IOError:
        return False
    return True
