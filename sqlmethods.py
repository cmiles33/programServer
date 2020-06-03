import mysql.connector
from mysql.connector import errorcode


class mySQLMethods:

    def __init__(self):

        try:
            self.cnx = mysql.connector.connect(user='caleb', password='password',
                                          host='192.168.1.24', database='myFirstData')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.cursor = self.cnx.cursor()

    def updateData(self, id, time, collumn):
        try:
            myCommand = "UPDATE contacts SET {} = '{}'" \
                        " WHERE id = '{}'".format(collumn, time, id)
            self.cursor.execute(myCommand)
            self.cnx.commit()
            return True
        except mysql.connector.Error as err:
            print(err.msg)
            return False

    def updateEnd(self, name, time):
        try:
            myCommand = "UPDATE contacts SET end = '{}'" \
                        " WHERE first_name = '{}'".format(time, name)
            self.cursor.execute(myCommand)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)

    def setPayload(self, id,payload):
        try:
            myCommand = "UPDATE contacts SET payload = '{}'" \
                        " WHERE id = '{}'".format(payload, id)
            self.cursor.execute(myCommand)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)

    def add_contact(self, first_name, last_name, phone_number='None', email='None'):
        try:
            command = '''
            INSERT
            INTO
            contacts(
                first_name,
                last_name,
                phone_number,
                email)

            VALUES
            ('{}', '{}', '{}', '{}');
            '''.format(first_name, last_name, phone_number, email)
            self.cursor.execute(command)
            self.cnx.commit()

        except mysql.connector.Error as err:
            print(err.msg)

    def closeConnections(self):
        self.cursor.close()
        self.cnx.close()

    def generalCommand(self,command):
        try:
            self.cursor.execute(command)
            print("Command Executed Sucessfully")
        except mysql.connector.Error as err:
            print(err.msg)

    def updateStatus(self, id, status):
        try:
            myCommand = "UPDATE contacts SET status = '{}'" \
                        " WHERE id = '{}'".format(status, id)
            self.cursor.execute(myCommand)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print(err.msg)



