
#### Getting the files
Download zip file or <br>
Clone with git + remove git folder
```
git clone https://github.com/jhasan0122/Build_It . && rm -rf .git
```
<br><br><br>



#### - Create Virtual Environment

###### # Windows
```
pip install virtualenv 
virtualenv venv 
```

```
venv\Scripts\activate
```

<br>




#### - Create new project
```
django-admin startproject project_name
```


#### - Create new apps
```
python manage.py startapp new_app_name
```


#### - Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

<br>

#### - Migrate to database
```
python manage.py makemigrations
python manage.py migrate
```

```
python manage.py createsuperuser
```

<br>

#### - Run application
```angular2html
python manage.py runserver
```

<br>

#### - Generate Secret Key ( ! Important for deployment ! )
```
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
exit()
```


### Save into requirement.txt 
```
source venv/bin/activate
pip freeze > requirements.txt
```

### Shell
```angular2html
python manage.py shell
```


