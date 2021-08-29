MobileShop - eCommerce website project using Python/Django framework
====================================================================

[![All Contributors](https://img.shields.io/badge/all_contributors-2-blue.svg?style=flat-square)](#contributors-)

Getting Started
------------

## From within the repo directory, first remove git tracking from the project  

```bash
$ rm -rf .git
```

## Initialize a new git repository:
```bash
$ git init
```

## Create new virtual enviroment
```bash
$ python3 -m venv venv
```

## Activate new virtual enviroment

Linux/MacOS:
```bash
$ source /venv/bin/activate
```
Windows:
```bash
$ .\venv\Scripts\Activate
```

## Install requirements:
```bash
$ pip install -r requirements.txt
```

## Make migrations:
```bash
$ python manage.py makemigrations
```

## Make migrate:
```bash
$ python manage.py migrate
```

## Run server:
```bash
$ python manage.py runserver
```

# Main page
![main_page](https://user-images.githubusercontent.com/81860226/131236405-0b4dd1a1-4df3-44c2-a0df-7648cd3c029a.png)

# All products page
![all_products](https://user-images.githubusercontent.com/81860226/131236406-e7cfe433-03a7-4962-9b5a-1b4f99b4642e.png)

# Guide page
![guide_page](https://user-images.githubusercontent.com/81860226/131236409-bd2df78f-6175-484a-89d2-1a75c708ef44.png)



Project Organization
------------
   
    ├── /README.md                 <- The top-level README for developers using this project.
    ├── /.gitignore                <- Files, where ignored files is added
    ├── /requirements.txt          <- The requirements file for PIP
    │
    └──/mobile_shop/               <- Python package directory for project
        |__/manage.py              <- A command-line utility that lets you interact with this Django project in various ways.
        │
        ├──/mobile_shop/           
        │   └── /settings.py       <- Django project settings
        |   |__ /asgi.py           <- An entry-point for ASGI-compatible web servers to serve your project.
        |   |__ /wsgi.py           <- An entry-point for WSGI-compatible web servers to serve your project. 
        |   |__ /urls.py           <- The URL declarations for this Django project; a “table of contents” of your Django-powered site.
        │
        ├──./shop                  <- Django App
        │   └──/views.py           <- controller (Logic)
        |   |__/admin.py           <- admin config
        |   |__/models.py          <- Data models
        |   |__/test.py            <- Test implementation
        |   |__/urls.py            <- URL config for view
        |   |__/migrations/        <- Data migration (auto)
        |   |__/static/            <- .css file storage
        |   |__/templates/         <- .html templates for registration, login, cart, etc. 
        |   |__/...
        │
        ├──./static/                <- .html/.css/.js files for bootstrap
        │   |__./...
        │   
        |__./templates/             <- .html templates for (base, footer, navbar, home) pages
                  |__./...

    
## Contributors ✨

<table>
  <tr>
    <td align="center"><a href="https://github.com/kstekels"><img src="https://avatars.githubusercontent.com/u/31929901?v=4" width="100px;" alt=""/><br /><sub><b>Karlis Stekels</b>
      </sub>
      </a>
    </td>
    <td align="center"><a href="https://github.com/jaz3ps"><img src="https://avatars.githubusercontent.com/u/77325378?v=4" width="100px;" alt=""/><br /><sub><b>Jazeps Ivulis</b>
      </sub>
      </a>
    </td>
  </tr>
</table>
