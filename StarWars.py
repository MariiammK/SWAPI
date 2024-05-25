import requests
import json
import sqlite3


#  გვაძლევს იმ პერსონაჟის შესახებ ინფორმაციას, რომელსაც შეესაბამება მითითებული ID
id = int(input("Enter ID of character: "))
# id = 45
url = f'https://swapi.dev/api/people/{id}/'


response = requests.get(url)

print("Response: ", response)
print("Status Code:", response.status_code)
print("Headers: ", response.headers)
print("Server: ", response.headers['Server'])
print("Date: ", response.headers['Date'])
print("Result in str format: ", response.text)

content = response.json()
print(json.dumps(content, indent=4))


#### json ფაილის შექმნა
file = open('SWA_data.json', 'w')
json.dump(content, file, indent=4)


#### json ფაილიდან ინფორმაციის წაკითხვა
# მთლიანი ინფორმაცია პერსონაჟის შესახებ
def all_info(c):
    print(json.dumps(c, indent=4))

# პერსონაჟის სახელი, სქესი და დაბადების თარიღი
def read_name_birth(c):
    print("Name: {} \nGender: {} \nBirth Year: {}\n".format(c["name"], c["gender"], c["birth_year"]))

# იმ ფილმების სახელები, რომლებშიც მონაწილეობდა აღნიშნული პერსონაჟი
def movies(c):
    m_list = c["films"]
    # რადგან ფილმები მოცემულია URL-ების სახით, ასეთი კოდი გვექნება:
    print("Movies that include this character: ")
    for i in m_list:
        m_response = requests.get(i)
        if m_response.status_code == 200:
            film = m_response.json()
            print(film["title"])
        else:
            print("Movies not fount or Error occured! ")


with open('SWA_data.json', 'r') as file:
    c = json.load(file)
    print(c)

    # მომხმარებლის სურვილის მიხედვით გამოიძახება აღნიშნული ფუნქციები:
    flag = int(input("Please enter the number: \n1. Return all info about character \n2. Only return Name, gender and birth year of the character \n3. names of the movies that include this character "))

    if flag == 1:
        all_info(c)
    elif flag == 2:
        read_name_birth(c)
    elif flag == 3:
        movies(c)
    else:
        print("incorrect input. ")


# მონაცემთა ბაზის შექმნა, პერსონაჟის შესახებ შემდეგი ინფორმაციის შესანახად: სახელი, სქესი, სიმაღლე
conn = sqlite3.connect('SWA_Database.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(100),
        Gender VARCHAR(50),
        Height VARCHAR(50)
    )
''')


character = (content["name"], content["gender"], content["height"])
c.execute("INSERT INTO characters (Name, Gender, Height) VALUES (?, ?, ?)", character)
conn.commit()


# ინფორმაციის დაბრუნება
# აბრუნებს იმ პერსონაჟთა სახელებს, რომელთა სქესიც არის მამრობითი:
gender = c.execute("SELECT * FROM characters WHERE Gender = 'male'")

for i in gender:
    print(i["Name"])

conn.close()