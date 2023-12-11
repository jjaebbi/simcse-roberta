def print_hi(name):
 # Use a breakpoint in the code line below to debug your

    print(f'Hi, {name}') # Press Ctrl+F8 to toggle the

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# TIBERO DB
import pyodbc
import numpy as np
import matplotlib.pyplot as plt
db = pyodbc.connect('DSN=aws_test_t6;UID=DAJOBA;PWD=DAJOBA' )
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM EMP")
for row in cursor:
    totalemps = int(row[0])
    print(totalemps)
t = np.arange(totalemps)
cursor.execute("select ename, sal from EMP")
enames = []
salaries = []
for row in cursor:
    totalemps = int(row[0])
    print(totalemps)
t = np.arange(totalemps)
cursor.execute("select ename, sal from EMP")
enames = []
salaries = []
for row in cursor:
    enames.append(row[0])
    salaries.append(row[1])
bar_width = 0.5
plt.bar(t, salaries, bar_width, label="Salary")
plt.title("Employee Details")
plt.xlabel("Employee")
plt.ylabel("Salary")
plt.xticks(t, enames)
plt.grid(True)
plt.legend()
xs = [x for x in range(1, totalemps)]
for x, y in zip(xs, salaries):
    plt.annotate(salaries[x], (x - bar_width / 2, y))
plt.show()