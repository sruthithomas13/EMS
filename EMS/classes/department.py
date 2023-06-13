from setup import mysql, session

class Department:
    def __init__(self,dept_id,dept_name):
        self.dept_id = dept_id
        self.dept_name = dept_name

    # Will fetch the department name by using the department id
    def fetchDeptName(self):
        mycursor = mysql.connection.cursor()
        try:
            query = 'SELECT DEPT_ID FROM DEPARTMENT_DETAILS WHERE DEPT_NAME = %s'
            values = (self.dept_name,)
            mycursor.execute(query,values)
            result = mycursor.fetchall()
            if result:
                dept_id = result[0][0]
                return True, dept_id
            else:
                dept_id = 0
                return False, dept_id
        except Exception as e:
            dept_id = 0
            mysql.connection.rollback()
            print(f'fetchDeptName | {e}')
            return False, dept_id

        finally:
            mycursor.close()

    # To select distinct department details from department table in the database
    def distinctDepartment(self):
        mycursor = mysql.connection.cursor()
        try:
            query = "SELECT DISTINCT DEPT_NAME,DEPT_ID FROM DEPARTMENT_DETAILS "
            mycursor.execute(query)
            result = mycursor.fetchall()
            if result:
                print("distinctDepartment | Department details fetched.")
                return result
            else:
                print("distinctDepartment | Failed to fetch department details.")
                return False
            
        except Exception as e:
            mysql.connection.rollback()
            print(f'distinctDepartment | {e}')
            return False
        
        finally:
            mycursor.close()
