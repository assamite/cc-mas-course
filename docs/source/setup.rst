Getting Started
===============

This page goes through basic setup of the development environment for Python.
We strongly encourage everybody to use similar approach, especially virtual
environments.

.. note::
	These instructions are made for Unix (and OSX). Some of the steps will
	not work on Windows. Should you encounter any problems, please try to solve
	them first by yourself, as the course staff does not have sufficient
	background on developing Python in Windows.

Installing Python 3.5.x
-----------------------

First, start by installing `Python 3.5 <https://www.python.org/downloads/release/python-352/>`_.
For OSX and Windows, the site offers installers. For Linux, follow the standard
procedure as described in the README::

	~$ ./configure
	~$ make
	~$ make test
	~$ sudo make install

In case you want to install Python without root (to be used, e.g. in Ukko),
use ``./configure prefix=path/to/install/folder``.

Configure $PATH
---------------

After the Python 3.5 is installed, you should configure your favorite shell to
include its installation directory in $PATH. This way, the interpreter (and
as is seen in next section, the virtual environment creating script) can be
invoked without tedious path mangling.

Creating a Virtual Environment
------------------------------

Creating `virtual environments <https://docs.python.org/3/library/venv.html>`_ in 
Python 3 is easy as it is a built-in feature. If your $PATH is properly
configured, just type::

	~$ pyvenv3.5 <venv>

And the script should do the rest. After the installation, you can enter the
virtual environment with::

	~$ source path/to/venv/bin/activate

And exit the virtual environment with::

	~$ deactivate


Installing the Requirements
---------------------------

We have included some packages that might come in handy in the `requirements.txt <>`_
in the github reposity. Install these packages when you have virtual environment
active::

	~$ source path/to/venv/bin/activate
	(venv) ~$ pip install -r requirements.txt


