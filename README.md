# WebDev Course object storage project

## Setup project for the first time

### Creating Virtual Environment and Installing Dependencies

[venv python doc](https://docs.python.org/3/library/venv.html)

- Linux

```sh
python -m venv venv
source venv/bin/activate
cd object_storage_server
pip install -r requirements.txt
```

[Python Tutorial: VENV (Mac & Linux) - Corey Schafer - YouTube](https://www.youtube.com/watch?v=Kg1Yvry_Ydk)

- Windows - Command Prompt

```cmd
python -m venv venv
.\venv\Scripts\activate
cd object_storage_server
pip install -r requirements.txt
```

[Python Tutorial: VENV (Windows) - Corey Schafer - YouTube](https://www.youtube.com/watch?v=APOPm01BVrk)

### Migrate the database

```sh
python manage.py makemigrations
python manage.py migrate
```

### Create superuser

```sh
python manage.py createsuperuser
```

### Add config.py

you need to add this for email authentication to work. (start from root of the project folder)

1- In object_storage_server/object_storage_server besides settings.py there is a file called config.py.example.

2- Copy the file into a new file in the same directory: config.py

3- Set the Email and Password of the email for the email authentication to work. (You can use [App passwords](https://support.google.com/accounts/answer/185833?hl=en&sjid=2203469487917550649-EU) for Gmail.)

## start using the project

For Linux

```sh
source venv/bin/activate
```

Or for Windows-cmd

```cmd
.\venv\Scripts\activate
```

And then

```sh
python manage.py runserver
```

hello Amina
