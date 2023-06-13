# Title: Employee Management System
# Author: Sruthi Ann Thomas
# Created on: 01-06-2023
# Last Modified Date: 12-06-2023
# Reviewed by: Naveen Subramaniam
# Reviewed on: 12-06-2023


from setup import render_template, request, redirect, url_for, session, app

from classes.personal import Personal
from classes.employee import Employee
from classes.department import Department
from classes.designation import Designation

# Initial startpoint of application              
@app.route('/')
def Initial():
    return redirect(url_for("Login"))

# To Login user credentials 
@app.route('/login', methods = ['GET','POST'])
def Login():
    if request.method == 'POST':
        action=request.form['action']
        if action == 'login':
            email = request.form['email']
            password = request.form['password']
            personal = Personal("","","","","","",email,password,"")
            validResult = personal.loginValidation()
            if(validResult):
                print("Login | Login successfull")
                return redirect(url_for('Homepage'))
            else:
                print("Login | Invalid Login")
                return render_template("login.html")

        else:
            print("Login | invalid")
            return render_template("login.html")
    else:
        return render_template("login.html")

# After Login is verified, user is directed to the homepage   
@app.route('/homepage')
def Homepage():
    if 'emp_id' not in session:
        return redirect (url_for('Login'))
    else:
        return render_template("homepage.html")

# User can add new employee details 
@app.route('/add-employee', methods = ['GET','POST'])
def addEmployee():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'add':
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            dob = request.form['dob']
            gender = request.form['gender']
            email = request.form['email']
            contact_no = request.form['contact_no']
            salary = request.form['salary']
            dept_id = request.form['dept_id']
            designation_id = request.form['designation_id']
            doj = request.form['doj']
            
            personal = Personal("",first_name,middle_name,last_name,dob,gender,email,"",contact_no)
            personalboolean, emp_id  = personal.addEmployee()
            if personalboolean:
                print("Personal details added")
                employee = Employee('','','','','','','','',emp_id,dept_id,designation_id,salary,doj,'','','','')
                employeeboolean = employee.addEmployee()
                if employeeboolean:
                    print("Success")
                    return redirect(url_for('addEmployee'))
                else:
                    print("Failure")
                    return redirect(url_for('addEmployee'))
            else:
                print("Failed to add personal details")
                return redirect(url_for('addEmployee'))
            
    if 'emp_id' not in session:
        return redirect (url_for('Login'))
    
    else:
        department = Department('','')
        dept_result = department.distinctDepartment()
        designation = Designation('','','','')
        desg_result = designation.distinctDesignation()   
        if dept_result:
            return render_template("reg.html", departmentDetails = dept_result, designationDetails = desg_result)
        else:
            return redirect (url_for('Login')) 

# User can view all exisitng employees and their details
@app.route('/view-employee', methods = ['GET','POST'])
def viewEmployee():
    if 'emp_id' not in session:
        return redirect (url_for('Login'))
    else:
        if request.method == 'POST':
            action = request.form['action']

            # User can delete any employee details that is offboarding from company   
            if action == 'delete':
                emp_id = request.form['emp_id']
                employee = Employee('','','','','','','','',emp_id,'','','','','','','','')
                result = employee.deleteEmployee()
                if result:
                    print("Delete Successfull")
                    return redirect(url_for("viewEmployee"))
                else:
                    print("Delete UNSuccessfull")
                    return redirect(url_for("viewEmployee"))
                
            else:
                return redirect (url_for('viewEmployee'))
        else:
            employees = Employee('','','','','','','','','','','','','','','','','')
            result=employees.viewEmployees()
            if result:
                print("View | successful")
                return render_template("view.html",employees=result)
            else:
                return redirect (url_for('viewEmployee'))

# User can view a specific employee details
@app.route('/view-specific-employee', methods = ['GET','POST'])
def viewSpecific():
    if 'emp_id' not in session:
        return redirect (url_for('Login'))
    else:
        if request.method == 'POST':
            action = request.form['action']
            if action == 'view':
                emp_id = request.form['emp_id']
                print(emp_id)
                employees = Employee('','','','','','','','',emp_id,'','','','','','','','')
                result=employees.viewSpecificEmployee()
                if result:
                    print("viewSpecific | successful")
                    return render_template("viewspecific.html",employees=result)
                else:
                    return redirect (url_for('viewSpecific'))
            else:
                return redirect (url_for('viewSpecific'))
        else:
            employees = Employee('','','','','','','','','','','','','')
            result=employees.viewEmployees()
            if result:
                print("viewEmployee | successful")
                return render_template("view.html",employees=result)
            else:
                return redirect (url_for('viewEmployee'))

# User can edit exisiting employee details by updating them     
@app.route('/edit-employee', methods=['GET', 'POST'])
def editEmployee():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'view':
            emp_id = request.form['emp_id']
            employees = Employee('','','','','','','','',emp_id,'','','','','','','','')
            result=employees.viewSpecificEmployee()
            if result:
                department = Department('','')
                dept_result = department.distinctDepartment()
                if dept_result:
                    designation = Designation('','','','')
                    desg_result = designation.distinctDesignation() 
                    if desg_result:
                        return render_template('edit.html', employeeDetails = result, designationDetails = desg_result, departmentDetails = dept_result)

        elif action == 'edit':
            emp_id = request.form['emp_id']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            dob = request.form['dob']
            gender = request.form['gender']
            email = request.form['email']
            contact_no = request.form['contact_no']
            dept_id = request.form['dept_id']
            designation_id = request.form['designation_id']
            salary = request.form['salary']
            doj = request.form['doj']
            orientation = request.form.get('orientation','Pending')
            training = request.form.get('training','Pending')
            credentials = request.form.get('credentials','Pending')
            equipment = request.form.get('equipment','Pending')

            orientation = 'Completed' if 'orientation' in request.form else 'Pending'
            training = 'Completed' if 'training' in request.form else 'Pending'
            credentials = 'Completed' if 'credentials' in request.form else 'Pending'
            equipment = 'Completed' if 'equipment' in request.form else 'Pending'

            employee = Employee(first_name,middle_name,last_name,dob,gender,email,'',contact_no,emp_id,dept_id,designation_id,salary,doj,orientation,training,credentials,equipment)
            result = employee.editEmployee(orientation,training,credentials,equipment)
            if result:
                return redirect(url_for("viewEmployee"))
            else:
                return redirect(url_for("viewEmployee"))
    else:
        return redirect(url_for("viewEmployee"))

# User can logout from homepage
@app.route('/logout')
def Logout():
    session.clear()
    return redirect (url_for('Login'))

if __name__ == '__main__':
    app.run(debug=True)
        
