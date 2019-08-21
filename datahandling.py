import hashlib


def load_data(name, c=' '):
    """load file (data_pi.py) """
    # returns dict of {hash: {'poly': poly}}
    name = 'data_' + name + '.txt'
    try:
        file = open(name, 'r')
    except FileNotFoundError:
        return {}
    data = [[[k for k in j.split(',')] for j in i[:-1].split(c)] for i in file]
    return {str(i[-1][0]): {'alpha': i[0],
                            'beta': i[1],
                            'gamma': i[2],
                            'delta': i[3]} for i in data}


def save_data(name, data, c=' '):
    """save file (data_pi.py) """
    # <hash>,<alpha>,<beta>,<gamma>,<delta>
    # 123...789 0,1 2,3 4,5 6,7
    name = 'data_' + name + '.txt'
    file = open(name, 'a')
    for i in data:
        s = c.join([','.join([str(k) for k in j]) if type(j) == list else str(j) for j in i])
        file.write(s + '\n')
    file.close()


def clear_data(name):
    """clear file"""
    name = 'data_' + name + '.txt'
    file = open(name, 'w')
    file.close()


def new_entry(name, hash_, alpha, beta, gamma, delta, c=' '):
    """add new unique data point (unique = new hash)"""
    database = load_data(name, c=c)
    if not str(hash_) in database:
        save_data(name, [[alpha, beta, gamma, delta, [hash_]]], c=c)


def show_data(name, c=' '):
    """clear file"""
    data = load_data(name, c=c)
    for I in data:
        print('\n')
        # print(I)
        for J in data[I]:
            print(' \t', J, '\t', data[I][J])


def hash_list(v):
    """ return hash of list """
    return int.from_bytes(hashlib.sha256(str(v).encode('utf-8')).digest(), 'big')   # decimal
    # return hashlib.sha256(str(v).encode('utf-8')).hexdigest()   # hexadecimal


if __name__ == '__main__':

    Name = 'test'
    clear_data(Name)

    new_entry(Name, hash_=1000, alpha=[2, 3], beta=[4, 5], gamma=[6, 7], delta=[8, 9])
    new_entry(Name, hash_=30000, alpha=[1, 2], beta=[3, 4], gamma=[5, 6], delta=[7, 8])
    new_entry(Name, hash_=1000, alpha=[2, 3], beta=[4, 5], gamma=[6, 7], delta=[8, 9])
    new_entry(Name, hash_=1000, alpha=[2, 3], beta=[4, 5], gamma=[6, 7], delta=[8, 9])
    new_entry(Name, hash_=1000, alpha=[2, 3], beta=[4, 5], gamma=[6, 7], delta=[8, 9])
    input()

    show_data(Name)
