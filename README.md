# note from django -->


1. create the folder of the project
2. open the terminal at that folder
3. create the virtual environment


    mac: pytohn3 -m venv venv
    windows: .\venv\Scripts\activate

4. activate virtual environment

    mac: source venv/bin/activate
    windows: .\venv\Scripts\activate

5. install the dependencies

    both OS:  pip3 install django

6. create django project structure

    both: django-admin startproject NAME_FOLDER .

7. python3 manage.py startapp NAME_FILE. 

8. Models in Django need to be written inside of the models.py file on any application when we finish them we need to run these commands:


    1. "python3 manage.py makemigrations" will create a migration interpreting the new models
    2. "python3 manage.py migrate" - Django will apply the created migration file to the database



touch FILENAME.EXENSION allows you to create files on the terminal.
mkdir FOLDERNAME makes folders in terminal
# 112-Django-intro
# 113-Django-intermediate


A.login/logout use path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    create 'login.html' and 'logged_out.html'