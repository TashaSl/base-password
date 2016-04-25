import sys
import pickle
import hashlib
import rsa

class password():
    def __init__(self):
        self.path = r'pass1.data'
        self.pub_key = None
        self.priv_key = None
        try:
            f = open(self.path, 'rb')
            file_content = pickle.load(f)
            self.pass_book = file_content
        except:
            self.pass_book = {}
        if type(self.pass_book) != dict or not self.pass_book:
            self.pass_book = {}
            self.create_user()
        else:
            self.checkuser()
    def create_user(self):
        password = input('\nПридумайте пароль доступа: ')
        while input('\nПовторите введенный пароль: ') != password:
            continue
        (self.pub_key, self.priv_key) = rsa.newkeys(512)
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        self.pass_book[password] = (self.pub_key, self.priv_key)
        print('Пользователь успешно создан')
        print('Для начала работы воспользуйтесь командой help')
        self.write_file()
        return self.enter()
    def checkuser(self):
        arg = input('\nВведите пароль доступа: ')
        arg = hashlib.md5(arg.encode('utf8')).hexdigest()
        if self.pass_book.get(arg):
            (self.pub_key, self.priv_key) = self.pass_book[arg]
            self.decrypt()
            return self.enter()
        else:
            print('Неправильный пароль')
            return self.checkuser()
    def decrypt(self):
        cpb = self.pass_book.copy()
        self.pass_book = {}
        for key in cpb:
            if cpb[key] != (self.pub_key, self.priv_key):
                key_decode = rsa.decrypt(key, self.priv_key).decode('utf8')
                self.pass_book[key_decode] = rsa.decrypt(cpb[key], self.priv_key).decode('utf8')
            else:
                self.pass_book[key] = cpb[key]
        del cpb
    def encrypt(self):
        cpb = self.pass_book.copy()
        self.pass_book = {}
        for key in cpb:
            if cpb[key] != (self.pub_key, self.priv_key):
                key_code = rsa.encrypt(key.encode('utf8'), self.pub_key)
                self.pass_book[key_code] = rsa.encrypt(cpb[key].encode('utf8'), self.pub_key)
            else:
                self.pass_book[key] = cpb[key]
        del cpb
    def enter(self):
        self.arg = input('\nВведите команду: ').split(' ')
        actions = ['add', 'edit', 'delete', 'find', 'show', 'help', 'change_pass']
        action = self.arg[0]
        if action == 'quit':
            self.write_file()
            return False
        if action in actions:
            getattr(self, action)()
        else:
            print('Незнакомая команда. Восполуйтесь командой help')
        return self.enter()
    def change_pass(self):
        try:
            self.arg[1] = rsa.decrypt(self.arg[1], self.priv_key)
            self.arg[2] = rsa.decrypt(self.arg[2], self.priv_key)
            old_passw = hashlib.md5(self.arg[1]).hexdigest()
            new_passw = hashlib.md5(self.arg[2]).hexdigest()
            if self.pass_book.getkey(old_passw):
                self.pass_book[new_passw] = self.pass_book[old_passw]
                del self.pass_book[old_passw]
            else:
                print('Неправильный пароль')
        except:
            print('Недостаточно аргументов')
    def add(self):
        try:
            if not self.arg[1] in self.pass_book:
                self.pass_book[self.arg[1]] = self.arg[2]
                print('Успешно добавлено')
            else:
                print('Уже существует')
        except:
            print('Недостаточно аргументов')
    def edit(self):
        try:
            if self.pass_book.get(self.arg[1]):
                self.pass_book[self.arg[1]] = self.arg[2]
                print('Успешно отредактировано')
            else:
                print('Такого нет')
        except:
            print('Недостаточно аргументов')
    def delete(self):
        try:
            if self.arg[1] in self.pass_book:
                del self.pass_book[self.arg[1]]
                print('Успешно удалено')
            else:
                print('Такого нет')
        except:
            print('Такого нет')
    def find(self):
        try:
            if self.arg[1] in self.pass_book:
                print(self.arg[1], ' ', self.pass_book[self.arg[1]])
            else:
                print('Такого нет')
        except:
            print('Недостаточно аргументов')
    def show(self):
        if self.pass_book == {}:
             print('Книга пуста')
        else:
            for key in self.pass_book:
                if self.pass_book[key] != (self.pub_key, self.priv_key):
                    print(key, '\t', self.pass_book[key])
    def help(self):
        print('Программа хранения паролей')
        print('Поддерживает следующие операции:')
        print('add key password')
        print('edit key password')
        print('delete key')
        print('find key')
        print('show')
        print('help')
        print('change_pass old_password new_password')
        print('key - от чего хранить пароль (без пробелов)')
        print('password - пароль (без пробелов)')
    def write_file(self):
        self.encrypt()
        f = open(self.path, 'wb')
        pickle.dump(self.pass_book, f)
        f.close()
app = password()
