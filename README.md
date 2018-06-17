# flask_project-per

## Flask


Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools. Extensions are updated far more regularly than the core Flask program.


## How To Serve Flask Applications with Gunicorn and Nginx on Ubuntu 16.04
### Introduction
In this guide, we will be setting up a simple Python application using the Flask micro-framework on Ubuntu 16.04. The bulk of this article will be about how to set up the Gunicorn application server to launch the application and Nginx to act as a front end reverse proxy.
### Install the Components from the Ubuntu Repositories
Our first step will be to install all of the pieces that we need from the repositories. We will install pip, the Python package manager, in order to install and manage our Python components. We will also get the Python development files needed to build some of the Gunicorn components. We'll install Nginx now as well.

Update your local package index and then install the packages. The specific packages you need will depend on the version of Python you are using for your project.

#### If you are using Python 2, type:
```
$ sudo apt-get update
$ python-pip python-dev nginx
```
