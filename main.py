import requests
import sqlite3

conn = sqlite3.connect("parsed.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

cursor.execute("""CREATE TABLE user
                  (id integer, name text, username text, reg_date DATE)
               """)

id = 0	  #id пользователя
name = []  # список для настоящего имени пользователя
username = [] # имя пользователя
reg_date = [] # дата регистрации
flag = False
commit_counter = 0
print('Starting process')

#address = 'http://www.sql-ex.ru/users_page.php?uid=69553'
while id <= 500000: # <= 500k пользователей на 16-6-2019

    address = 'http://www.sql-ex.ru/users_page.php?uid=' + str(id)
    r = requests.get(address)  #получаем данные реквеста - в случае с доками - html код
    info = str(r.content)  #получаем строку с хтмл

    point = info.find('<td valign=bottom>')
    act_point = point + 18
    if point != (-1):
        flag = True
        while act_point < len(info):
            if info[act_point] == '<':
                break
            name.append(info[act_point])
            act_point += 1
        name = ''.join(name)

    if (flag):
        point = info.find('Registration date')
        act_point = point + 19
        if point != (-1):
            while act_point < len(info):
                if info[act_point] == '<':
                    break
                reg_date.append(info[act_point])
                act_point += 1
            reg_date = ''.join(reg_date)

            if(reg_date):
                reg_date_split = reg_date.split('.')
                reg_date=[]
                reg_date.append(reg_date_split[2])
                reg_date.append('-')
                reg_date.append(reg_date_split[1])
                reg_date.append('-')
                reg_date.append(reg_date_split[0])
                reg_date = ''.join(reg_date)

        point = info.find('Information about professional ')
        act_point = point + 31
        if point != (-1):
            while act_point < len(info):
                if info[act_point] == '<':
                    break
                username.append(info[act_point])
                act_point += 1
            username = ''.join(username)

        point = info.find('Information about user ')
        act_point = point + 23
        if point != (-1):
            while act_point < len(info):
                if info[act_point] == '<':
                    break
                username.append(info[act_point])
                act_point += 1
            username = ''.join(username)

    if (username):
        #print(str(id) + ' ' + str(name) + ' ' + str(reg_date) + ' ' + str(username))
        cursor.execute('''INSERT INTO user(id, name, username, reg_date)
                          VALUES(?,?,?,?)''', (id, name, username, reg_date))
        commit_counter += 1
        if (commit_counter == 50):
            conn.commit()
            print('commit ok, last commited id = ' + str(id))
            commit_counter = 0
    name = []
    reg_date = []
    username = []
    flag = False
    id += 1
