# Glide-Ez_New

### SETUP:

---

**Step1:** Python installed

- check version (python3 --version )
- check pip (py -m pip --version)<br>

---

**Step2:** Setup Virtual environment

- py -m pip install virtualenv
- python -m virtualenv env
- cd env
- cd Scripts
- .\activate.bat
- cd ..
- env\Scripts\activate
- to deactivate just type deactivate <br>

---

**Step3:** Install django

- make sure you're in your virtual env first.
- py -m pip install django
- py -m manage runserver<br>

---

**Step4:** Setup mysql

- Install mysqlclient(Before this Step update the Databases list in settings.py)
- py -m pip install mysql-connector-python
- py -m pip install mysqlclient
- py -m manage migrate<br>

---

### OPTIONAL

**Enviornment variables**

- py -m pip install django-environ
- py -m pip install --upgrade sweetify

