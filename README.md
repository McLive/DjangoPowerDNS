# DjangoPowerDNS

DjangoPowerDNS is a new PowerDNS webinterface written in Python and powered by Django.


## Features

  - Add/Edit/Remove DNS records easily
  - Use the REST-API to change DNS records within your application
  - Add users to certain domains to allow them editing DNS records

___

### Tech

DjangoPowerDNS uses awesome open source tools!

* [Django](https://www.djangoproject.com/)
* [Knockout.js](http://knockoutjs.com/)
* [Twitter Bootstrap](http://getbootstrap.com/)
* [SweetAlert](https://sweetalert.js.org/)
* [Bootstrap Notify](http://bootstrap-notify.remabledesigns.com/)
* [Navigo](https://github.com/krasimir/navigo)

___

### Screenshots

|  |   |
|:-------------:|:-------------:|
|![Domain list](https://dr0p.it/Ckam.png "Domain list")|![Records list](https://dr0p.it/ISG9.png "Records list")|
|![API preview](https://dr0p.it/p3tI.png "API preview")||
|  |   |

___

### Installation
Install the following dependencies:

```sh
$ apt update
$ apt install python2.7
$ apt install python-pip
$ apt install git
$ apt install uwsgi
$ apt install python-mysqldb
$ apt install mysql-client
For mariadb:
$ apt install libmariadbclient-dev
```

Clone the repository
```sh
$ git clone https://github.com/McLive/DjangoPowerDNS.git
```

Install and setup the virtualenv
```sh
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
```

Install the python requirements
```sh
$ pip install -r requirements.txt
```

* Rename `DjangoPowerDNS/settings.py.dist` to `DjangoPowerDNS/settings.py`
* Change MySQL settings and secret key in `DjangoPowerDNS/settings.py`

Apply migrations
```sh
$ python manage.py migrate
```

Create a superuser
```sh
$ python manage.py createsuperuser
```

___


### Todos

 - Complete README.md :)
 - Please send feature requests