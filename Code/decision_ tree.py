import mysql.connector
from sklearn import tree


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="user",
  passwd="password",
  database='database'
)
x, y = [], []

cursor = mydb.cursor()
query = 'SELECT * FROM tablename;'
cursor.execute(query)

for (model, year, price) in cursor:
    item = price, year
    x.append(list(item))
    y.append(model)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
a, b = tuple(map(int, input('please enter price and year:').split()))
data = [[a, b]]
answer = clf.predict(data)
print(answer[0])

