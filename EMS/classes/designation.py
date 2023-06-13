from setup import mysql, session
from classes.department import Department

# class designation inherits class department
class Designation(Department):
    def __init__(self, dept_id, dept_name, designation_id, designation_name):
        super().__init__(dept_id, dept_name)
        self.designation_id = designation_id
        self.designation_name = designation_name

    # Will fetch the designation name by using the designation id
    def fetchDesignationName(self):
        mycursor = mysql.connection.cursor()
        try:
            query = 'SELECT DESIGNATION_ID FROM DESIGNATION_DETAILS JOIN DEPARTMENT_DETAILS ON DEPARTMENT_DETAILS.DEPT_ID = DESIGNATION_DETAILS.DEPT_ID WHERE DESIGNATION_DETAILS.DESIGNATION_NAME = %s AND DEPARTMENT_DETAILS.DEPT_ID = %s'
            values = (self.designation_name,self.dept_id)
            mycursor.execute(query,values)
            result = mycursor.fetchall()
            if result:
                designation_id = result[0][0]
                return True, designation_id
            else:
                designation_id = 0
                designation_name = 0
                return False, designation_id
        except Exception as e:
            mysql.connection.rollback()
            designation_id = 0
            
            print(f'fetchDesignationName | {e}')
            return False, designation_id
        finally:
            mycursor.close()
        
    # To select distinct designation details from designation table in the database   
    def distinctDesignation(self):
        mycursor = mysql.connection.cursor()
        try:
            query = 'SELECT DISTINCT DESIGNATION_NAME, DESIGNATION_ID FROM DESIGNATION_DETAILS JOIN DEPARTMENT_DETAILS ON DEPARTMENT_DETAILS.DEPT_ID = DESIGNATION_DETAILS.DEPT_ID'
            mycursor.execute(query)
            result = mycursor.fetchall()
            if result:
                print("distinctDesignation | Designation details fetched.")
                return result
            else:
                print("distinctDesignation | Failed to fetch designation details.")
                return False
            
        except Exception as e:
            mysql.connection.rollback()
            print(f'distinctDesignation | {e}')
            return False
        
        finally:
            mycursor.close()
 