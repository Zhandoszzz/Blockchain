import hashlib
import json
import os


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = self.build_tree()

    def build_tree(self):
        if len(self.transactions) % 2 != 0:
            self.transactions.append(self.transactions[-1])

        tree = [hashlib.sha256((t1 + t2).encode()).hexdigest()
                for t1, t2 in zip(self.transactions[::2], self.transactions[1::2])]

        if len(tree) > 1:
            return self.build_tree()
        return tree

    def get_root(self):
        return self.tree[0]


def get_hash(filename):
    path = os.curdir + '/blockchain/'
    file = open(path + filename, 'rb').read()
    return hashlib.sha256(file).hexdigest()


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
    if filename > 1:
        prev_hash = get_hash(last_filename)
    info = {
        'sender': sender,
        'receiver': receiver,
        'amount': amount,
        'hash': prev_hash
    }
    with open(path + str(filename), 'w') as file:
        file.write(json.dumps(info))
    print(f'Block {filename} created')


def main():
    print('!writeblock - adds block')
    print('!validate - to check integrity')
    while True:
        commands = input()
        try:
            if commands[0] == '!':
                commands = commands[1:].split()
                for x in commands:
                    if x == 'writeblock':
                        sender = input('Sender:')
                        receiver = input('Receiver:')
                        amount = input('Amount:')
                        write_block(sender, receiver, amount)
                    elif x == 'validate':
                        validate()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
    validate()
