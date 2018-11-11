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
* [toastr](https://github.com/CodeSeven/toastr)
* [Navigo](https://github.com/krasimir/navigo)

___

### Screenshots

|  |   |
|:-------------:|:-------------:|
|![Domain list](https://upl0ad.cloud/K738.png "Domain list")|![Records list](https://upl0ad.cloud/EtIL.png "Records list")|
|![API preview](https://upl0ad.cloud/1pVW.png "API preview")||
|  |   |

___

### Installation
Install the following dependencies:

On Debian based Systems:
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

On RHEL based Systems: 
```sh
$ yum update -y
$ yum install -y python
$ yum install -y python-pip
$ yum install -y git
$ yum install -y uwsgi
$ yum install -y MySQL-python
$ yum install -y python-devel
$ yum install -y mariadb-devel
$ yum install libxslt-devel libxml2-devel
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
