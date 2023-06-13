from setup import mysql, session

class Personal:
    def __init__(self,emp_id,first_name,middle_name,last_name,dob,gender,email,password,contact_no):
        self.emp_id = emp_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.email = email
        self.password = password
        self.contact_no = contact_no

    # Checks the user login validation
    def loginValidation(self):
        mycursor = mysql.connection.cursor()
        try:
            query = 'SELECT * FROM PERSONAL_DETAILS WHERE EMAIL = %s AND PASSWORD = %s' 
            values = (self.email,self.password)
            mycursor.execute(query,values)
            result = mycursor.fetchall()
            if result:
                for row in result:
                    id = row[0]
                    email = row[6]
                    session['emp_id'] = id
                    session['emp_email'] = email
                return True
            else:
                return False
        except Exception as e:
            mysql.connection.rollback()
            print(f"loginValidation | {e}")
            return False
        finally:
            mycursor.close()

    # Checks if the employee already exists in the database
    def employeeExistence(self):
        mycursor = mysql.connection.cursor()
        try:
            query ='SELECT * FROM PERSONAL_DETAILS WHERE EMAIL= %s'
            values = (self.email,)
            mycursor.execute(query,values)
            result = mycursor.fetchall()
            if result:
                print("employeeExistence | employee exists")
                return False
            else:
                return True
        except Exception as e:
            mysql.connection.rollback()
            print(f"employeeExistence | {e}")
            return False
        finally:
            mycursor.close()

    # To add new employee details into the database
    def addEmployee(self):
        mycursor = mysql.connection.cursor()
        try:
            query = 'INSERT INTO PERSONAL_DETAILS(FIRST_NAME,MIDDLE_NAME,LAST_NAME,DOB,GENDER,EMAIL,CONTACT_NO) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            values = (self.first_name,self.middle_name,self.last_name,self.dob,self.gender,self.email,self.contact_no)
            mycursor.execute(query,values)
            mysql.connection.commit()
            if mycursor.rowcount > 0:
                query = 'SELECT LAST_INSERT_ID() AS EMP_ID'
                mycursor.execute(query)
                result = mycursor.fetchall()
                if result:
                    emp_id = result[0][0]
                    return True, emp_id
                else:
                    emp_id = 0
                    return False, emp_id
            else:
                emp_id = 0
                return False, emp_id
        except Exception as e:
            emp_id = 0
            mysql.connection.rollback()
            print(f"addEmployee | {e}")
            return False, emp_id
        finally:
            mycursor.close()
        