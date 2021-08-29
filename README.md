MobileShop - eCommerce website project using Python/Django framework
====================================================================

[![All Contributors](https://img.shields.io/badge/all_contributors-2-blue.svg?style=flat-square)](#contributors-)

Getting Started
------------

From within the repo directory, first remove git tracking from the project  

```bash
rm -rf .git
```

Initialize a new git repository:
```bash
git init
```

Create new virtual enviroment
```bash
python3 -m venv venv
```

Activate new virtual enviroment
Linux/MacOS:
```bash
source /venv/bin/activate
```
Windows:
```bash
.\venv\Scripts\Activate
```

Install requirements:
```bash
pip install -r requirements.txt
```

Run server:
```bash
python manage.py runserver
```




Project Organization
------------
   ...
    ├── ./README.md                 <- The top-level README for developers using this project.
    ├── ./.gitignore                <- Files, where ignored files is added
    ├── ./requirements.txt          <- The requirements file for PIP
    │
    └──./mobile_shop/               <- Python package directory for project
        |__./manage.py              <- A command-line utility that lets you interact with this Django project in various ways.
        │
        ├──./mobile_shop/           
        │   └── ./settings.py       <- Django project settings
        |   |__ ./asgi.py           <- An entry-point for ASGI-compatible web servers to serve your project.
        |   |__ ./wsgi.py           <- An entry-point for WSGI-compatible web servers to serve your project. 
        |   |__ ./urls.py           <- The URL declarations for this Django project; a “table of contents” of your Django-powered site.
        │
        ├──./shop                   <- Django App
        │   └──./views.py           <- controller (Logic)
        |   |__./admin.py           <- admin config
        |   |__./models.py          <- Data models
        |   |__./test.py            <- Test implementation
        |   |__./urls.py            <- URL config for view
        |   |__./migrations/        <- Data migration (auto)
        |   |__./static/            <- .css file storage
        |   |__./templates/         <- .html templates for registration, login, cart, etc. 
        |   |__./...
        │
        ├──./static/                <- .html/.css/.js files for bootstrap
        │   |__./...
        │   
        |__./templates/             <- .html templates for (base, footer, navbar, home) pages
s            |__./...

    
## Contributors ✨

<table>
  <tr>
    <td align="center"><a href="https://github.com/kstekels"><img src="https://avatars.githubusercontent.com/u/31929901?v=4" width="100px;" alt=""/><br /><sub><b>Christian Erhardt</b>
      </sub>
      </a>
    </td>
    <td align="center"><a href="https://github.com/jaz3ps"><img src="https://avatars.githubusercontent.com/u/77325378?v=4" width="100px;" alt=""/><br /><sub><b>Jeff Billimek</b>
      </sub>
      </a>
    </td>
  </tr>
</table>
