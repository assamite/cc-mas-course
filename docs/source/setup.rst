Setup Development Environment
=============================

This page goes through basic setup of the development environment for Python.
We strongly encourage the use of virtual environments (see below).

.. note::
	These instructions are made for Linux and OSX.

Installing Python 3.5.x
-----------------------

First, start by installing `Python 3.5 <https://www.python.org/downloads/release/python-352/>`_.
The site offers installers for OSX and Windows. In Linux, follow the standard
procedure as described in the README:

.. code-block:: console

	~$ ./configure
	~$ make
	~$ make test
	~$ sudo make install


.. note::
	In case you want to install Python without root (to be used, e.g. in Ukko-cluster),
	use ``./configure prefix=path/to/install/folder``.


Creating a Virtual Environment
------------------------------

`Virtual environments <https://docs.python.org/3/library/venv.html>`_ allow
multiple Python installations with conflicting package version requirements, etc.,
to co-exist peacefully on the same machine.

Creating virtual environments in Python 3.5 is easy as it is a built-in feature.
The script is called ``pyvenv-3.5`` and it is in the ``bin`` folder of the
Python installation location. Execute the script in the folder where you want
your virtual environment to be created with the name of the virtual environment
as the parameter, e.g::

	~$ pyvenv-3.5 venv

And the script should do the rest. After the installation, you can enter the
virtual environment by executing its ``activate``-script::

	~$ source path/to/venv/bin/activate

Now you should be able to enter Python 3.5 interpreter by typing ``python`` no
matter what base Python you have installed in your computer.

To exit the virtual environment type::

	~$ deactivate


Installing the Requirements
---------------------------

We have included the packages that are required by the examples and some convenience
packages in
`requirements.txt <https://github.com/assamite/cc-mas-course/blob/master/requirements.txt>`_
in the github repository. Clone the github repository or download the file, and
install these packages with `pip <https://pip.pypa.io/en/stable/>`_
once you have virtual environment active (virtual environment is bundled with
pip by default so there is no need to manually install it). ::

	~$ source path/to/venv/bin/activate
	(venv) ~$ pip install -r requirements.txt

.. note::
	We may add additional requirements during the course. However, they should
	be clearly noted when needed.

Text Editor
-----------

Use your favorite text editor which has Python support. Some examples include:

	- `PyCharm <https://www.jetbrains.com/pycharm/>`_
	- `Sublime Text <https://www.sublimetext.com/>`_
	- `Eclipse <https://eclipse.org/>`_ with `PyDev <http://www.pydev.org/>`_
