# peerxp_assessment

1) first you want to pip install requirements.txt file that i will freeze pip
2) then you can choose which database you want to use 
     - if sqlite3 set it default 
     - if postgresql
        1)  go to manage.py
        2) i have initialized a variable called VENV change its path to dev 
        3) ./manage.py makemigrations
           ./manage.py migrate
           ./manage.py runserver
           
 3) there you can see 2 files inside settings 
   - one for local and dev for production we use postgresql in production
   
   
 
   
