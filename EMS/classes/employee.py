from setup import mysql, session
from classes.personal import Personal

# class employee inherits class Personal
class Employee(Personal):
    def __init__(self,first_name,middle_name,last_name,dob,gender,email,password,contact_no,emp_id,dept_id,designation_id,salary,doj,orientation,training,credentials,equipment):
        super().__init__(emp_id,first_name,middle_name,last_name,dob,gender,email,password,contact_no)
        self.dept_id = dept_id
        self.designation_id = designation_id
        self.salary = salary
        self.doj = doj
        self.orientation = orientation
        self.training = training
        self.credentials = credentials
        self.equipment = equipment

    # To add new employee details into the database using method overriding
    def addEmployee(self):
        mycursor = mysql.connection.cursor()

        try:
            query = 'INSERT INTO EMPLOYEE_DETAILS(EMP_ID,DEPT_ID,DESIGNATION_ID,SALARY,DOJ) VALUES (%s,%s,%s,%s,%s)'
            values = (self.emp_id,self.dept_id,self.designation_id,self.salary,self.doj)
            mycursor.execute(query,values)
            mysql.connection.commit()
            if mycursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            mysql.connection.rollback()
            print(f"employeeExistence | {e}")
            return False
        finally:
            mycursor.close()
    
    # To view exisiting employees in the database
    def viewEmployees(self):
        mycursor = mysql.connection.cursor()
        try:
            query = 'SELECT PERSONAL_DETAILS.*, EMPLOYEE_DETAILS.SALARY, EMPLOYEE_DETAILS.DOJ, DEPARTMENT_DETAILS.DEPT_NAME, DESIGNATION_DETAILS.DESIGNATION_NAME, EMPLOYEE_DETAILS.ORIENTATION, EMPLOYEE_DETAILS.TRAINING, EMPLOYEE_DETAILS.CREDENTIALS, EMPLOYEE_DETAILS.EQUIPMENT FROM PERSONAL_DETAILS INNER JOIN EMPLOYEE_DETAILS ON EMPLOYEE_DETAILS.EMP_ID = PERSONAL_DETAILS.EMP_ID INNER JOIN DEPARTMENT_DETAILS ON DEPARTMENT_DETAILS.DEPT_ID = EMPLOYEE_DETAILS.DEPT_ID INNER JOIN DESIGNATION_DETAILS ON DESIGNATION_DETAILS.DESIGNATION_ID = EMPLOYEE_DETAILS.DESIGNATION_ID'
            mycursor.execute(query)
            result = mycursor.fetchall()
            if result:
                return result
            else:
                return False
        except Exception as e:
            mysql.connection.rollback()
            print(f'viewEmployees | {e}')
            return False
        finally:
            mycursor.close()
    
    # To view specific employee details in the database
    def viewSpecificEmployee(self):
        mycursor = mysql.connection.cursor()
        try:
            query = 'SELECT PERSONAL_DETAILS.*, EMPLOYEE_DETAILS.SALARY, EMPLOYEE_DETAILS.DOJ, DEPARTMENT_DETAILS.DEPT_NAME, DESIGNATION_DETAILS.DESIGNATION_NAME,EMPLOYEE_DETAILS.ORIENTATION, EMPLOYEE_DETAILS.TRAINING, EMPLOYEE_DETAILS.CREDENTIALS, EMPLOYEE_DETAILS.EQUIPMENT FROM PERSONAL_DETAILS INNER JOIN EMPLOYEE_DETAILS ON EMPLOYEE_DETAILS.EMP_ID = PERSONAL_DETAILS.EMP_ID INNER JOIN DEPARTMENT_DETAILS ON DEPARTMENT_DETAILS.DEPT_ID = EMPLOYEE_DETAILS.DEPT_ID INNER JOIN DESIGNATION_DETAILS ON DESIGNATION_DETAILS.DESIGNATION_ID = EMPLOYEE_DETAILS.DESIGNATION_ID WHERE EMPLOYEE_DETAILS.EMP_ID = %s'
            values = (self.emp_id,)
            mycursor.execute(query,values)
            result = mycursor.fetchall()
            if result:
                print("id fetched")
                return result
            else:
                print("id not fetched")
                return False
        except Exception as e:
            mysql.connection.rollback()
            print(f'viewSpecificEmployee | {e}')
            return False
        finally:
            mycursor.close()
    
    # To modifiy employee details
    def editEmployee(self,orientation,training,credentials,equipment):
        mycursor = mysql.connection.cursor()
        try:
            query = 'UPDATE PERSONAL_DETAILS INNER JOIN EMPLOYEE_DETAILS ON EMPLOYEE_DETAILS.EMP_ID = PERSONAL_DETAILS.EMP_ID SET PERSONAL_DETAILS.FIRST_NAME = %s, PERSONAL_DETAILS.MIDDLE_NAME = %s,  PERSONAL_DETAILS.LAST_NAME = %s, PERSONAL_DETAILS.DOB = %s, PERSONAL_DETAILS.GENDER = %s, PERSONAL_DETAILS.EMAIL = %s, PERSONAL_DETAILS.CONTACT_NO = %s, EMPLOYEE_DETAILS.DEPT_ID = %s, EMPLOYEE_DETAILS.DESIGNATION_ID = %s, EMPLOYEE_DETAILS.SALARY = %s, EMPLOYEE_DETAILS.DOJ = %s, EMPLOYEE_DETAILS.ORIENTATION = %s, EMPLOYEE_DETAILS.TRAINING = %s, EMPLOYEE_DETAILS.CREDENTIALS = %s, EMPLOYEE_DETAILS.EQUIPMENT = %s WHERE PERSONAL_DETAILS.EMP_ID = %s'
            values = (self.first_name,self.middle_name,self.last_name,self.dob,self.gender,self.email,self.contact_no,self.dept_id,self.designation_id,self.salary,self.doj,orientation,training,credentials,equipment,self.emp_id)
            mycursor.execute(query,values)
            mysql.connection.commit()
            if mycursor.rowcount > 0:
                print("Edit emp successfull")
                return True
            else:
                print("Edit emp unsuccessfull")
                return False
        except Exception as e:
            mysql.connection.rollback()
            print(f"editEmployee | {e}")
            return False
        finally:
            mycursor.close()
    
    # To delete exisiting employees from the database
    def deleteEmployee(self):
        mycursor = mysql.connection.cursor()
        try:
            mycursor.callproc("delete_employee", [self.emp_id])
            mysql.connection.commit()
            if mycursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            mysql.connection.rollback()
            print(f"deleteEmployee | {e} ")
            return False
        finally:
            mycursor.close() 
