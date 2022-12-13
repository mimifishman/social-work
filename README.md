

# Social-Work
#### Video Demo: https://youtu.be/OBBYyn77TrI

This web application is intended to streamline the process of the hybrid work model, while allowing the employee to create a work-life balance.
Employers can attract top talent by giving them the benefits of flexibility and enable employees to work within a social environment that inspires them. 


## Technologies
***
* Flask Framework:  Version 2.0
* Python: Version 3.10
* Jinja: Version 3.0
* SQLite: Version 3.37 
* Bootstrap: Version 4


## How the web applications works
***
* Cafe/Vendors signup to become a host work space
    * Today this is done behind the scenes without a UI, this will be developed in the next version.
* Businesses sign up to be part of the social-work environment, enabling their employees to book tables and meals at a local café.   
* Employees sign up and make a reservation at a cafe of their choosing.
* Employees can set their profile to public, thereby enabling them to view others who have made a reservation at a café.


## Application Usage 
***
* **Businesses** 
    * Company Registration - Register your company (At this time a representative will call for payment options.)
    * Employee Management - Once a company is registered and employees start to sign up the employees can be viewed.
        - Approve the employee by checking the approval checkbox and clicking Update, in addition you can un-approve 
          an employee by unchecking approval. 
        - Employees will be unable to make a cafe reservation if they are not approved. 
        - You can search the list for an employee, filter the data and sort. 
* **Employees** (Users)  
    * Employee Registration - Register under the company you work for.
    * The Cafes - Signup or view others that have made a reservation at a specific cafe by clicking on a cafe (cafes are sorted by distance),
      which will take you the cafe's sign up page. 
    * Cafe_Signup 
        - To sign up for a cafe, enter the date, start time and end time and click Submit
        - View others who have made a reservation at the cafe. You can search the list of names, filter by date and time and sort.  
* **General**
    * Login - Login with email and password
    * Account Update - Make changes to your Account.
    * Password Update - Change your password.
    * Log Out - Clear your user session.

## Sessions for Routing 
***
* user_id for all users
* company_id for company logins 

## Database Tables
*** 
* user_type - Specifies the type of user - customer, vendor, employee
* user - User information 
* company_type - Specifies the type of company - customer, vendor
* company - Company information for customers and vendors 
* geo_location - latitude and longitude of each user, used in cafe distance 
* cafe-signup - cafe reservations. 
* countries - List of countries used in the registration form.

## Python Files
***
* app.py - Main routing file. 
* helpers.py -  Helper functions.
* forms.py - WTforms forms.


## Future Developments
***
* UI for cafes/vendors
* Price list for cafe reservations and meal plans
* Companies select meal plan per employee 
* Companies payment and invoice
* Enable employees to search for a specific person at any cafe.
* Show companies their employee's hours. 





















