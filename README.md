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

#### If you are using Python 3, type:
```
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev nginx
```

## Create a Python Virtual Environment
Next, we'll set up a virtual environment in order to isolate our Flask application from the other Python files on the system.

Start by installing the ```virtualenv``` package using ```pip```.

#### If you are using Python 2, type:

```
$ sudo pip install virtualenv
```

#### If you are using Python 3, type:

``` 
$ sudo pip3 install virtualenv
```
Now, we can make a parent directory for our Flask project. Move into the directory after you create it:

```
$ mkdir ~/myproject
$ cd ~/myproject
```
We can create a virtual environment to store our Flask project's Python requirements by typing:

```
$ virtualenv myprojectenv
```
This will install a local copy of Python and ```pip``` into a directory called ```myprojectenv``` within your project directory.

Before we install applications within the virtual environment, we need to activate it. You can do so by typing:

```
$ source myprojectenv/bin/activate
```
Your prompt will change to indicate that you are now operating within the virtual environment. It will look something like this ```(myprojectenv)user@host:~/myproject$```.


