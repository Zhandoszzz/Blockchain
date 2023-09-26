import hashlib
import json
import os


def get_hash(filename):
    path = os.curdir + '/blockchain/'
    file = open(path + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()


def validate():
    path = os.curdir + '/blockchain/'
    files = os.listdir(path)
    for filename in files[1:]:
        file = open(path + filename)
        hash = json.load(file)['hash']
        file_n = int(filename)
        real_hash = get_hash(str(file_n - 1))
        result = 'Not valid' if hash != real_hash else 'Valid'
        print(f'Block {file_n - 1}: {result}')


def write_block(sender, receiver, amount, prev_hash=''):
    path = os.curdir + '/blockchain/'
    last_filename = os.listdir(path)[-1] if len(os.listdir(path)) > 0 else '0'

    filename = int(last_filename) + 1
    if filename == '1':
        prev_hash = get_hash(last_filename)
    info = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'hash': prev_hash
    }
    with open(path + str(filename), 'w') as file:
        file.write(json.dumps(info))


def main():
    write_block('A', 'B', 10, '')


if __name__ == "__main__":
    main()
    validate()