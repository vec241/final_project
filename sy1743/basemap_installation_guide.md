## Installation
basemap and GEOS (Geometry Engine - Open Source) library are required for showing features on the map, both two libraries are already downloaded in the compressed file: **basemap-1.0.7.tar.gz**.
The below instructions are referenced from:              http://matplotlib.org/basemap/users/installing.html
### step 1: Numpy, python and matplotlib
Install numpy 1.0.0 or later, python 2.4 or later, matplotlib 1.0.0 or later. **If they are installed, go to step2**.
### step 2: Untar the file
Untar the basemap-1.0.7.tar.gz file in the folder **resource**, and and cd to the **basemap-1.0.7** directory
### step 3: Install GEOS library
**1 If you don’t have GEOS library on your system**, you can build it from the source code included with basemap by using following commands in the ubuntu command line:
* cd to the geos-3.3.3 directory (it is under the directory basemap-1.0.7)
```sh
$ cd geos-3.3.3
```
* setting environment variable GEOS_DIR and Install the GEOS library
```sh
$ export GEOS_DIR=<the directory you want the libs and headers to go> 
##I recommend to install it in your home directory, for example:/home/ds-ga-1007
##Do not have space before and after the '=' symbol, a correct example is like this: export GEOS_DIR=/home/ds-ga-1007
##If any permission wrong happens, use sudo su to get the super user authority, or get root authority

$ ./configure --prefix=$GEOS_DIR
##I recommend you to get super user authority here
##The result of this command is like: 
##Swig: false 
##Python bindings: false
##...

$ sudo su ##then enter the password to get super user authority
$ make; make install ## It may take a bit time, ignore the warnings if any
```

**2 If you already have GEOS library on your system**, just set the environment variable GEOS_DIR to point to the location of libgeos_c and geos_c.h (if libgeos_c is in /usr/local/lib and geos_c.h is in /usr/local/include, set GEOS_DIR to /usr/local). Then go to next step. 

### step 4: Install basemap
cd back to the top level basemap directory (**basemap-1.0.7**) and run the usual **python setup.py install**. Check your installation by running **from mpl_toolkits.basemap import Basemap** at the python prompt.
```sh
$ cd basemap-1.0.7
#make sure you have super user authority 
$ sudo su
$ python setup.py install

##Check whether you have installed successfully
$ python
$ from mpl_toolkits.basemap import Basemap 
##If this works, the installation is OK
```





# Dillinger

Dillinger is a cloud-enabled, mobile-ready, offline-storage, AngularJS powered HTML5 Markdown editor.

  - Type some Markdown on the left
  - See HTML in the right
  - Magic

Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Version
3.2.0

### Tech

Dillinger uses a number of open source projects to work properly:

* [AngularJS] - HTML enhanced for web apps!
* [Ace Editor] - awesome web-based text editor
* [Marked] - a super fast port of Markdown to JavaScript
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [node.js] - evented I/O for the backend
* [Express] - fast node.js network app framework [@tjholowaychuk]
* [Gulp] - the streaming build system
* [keymaster.js] - awesome keyboard handler lib by [@thomasfuchs]
* [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

### Installation

You need Gulp installed globally:

```sh
$ npm i -g gulp
```

```sh
$ git clone [git-repo-url] dillinger
$ cd dillinger
$ npm i -d
$ mkdir -p downloads/files/{md,html,pdf}
$ gulp build --prod
$ NODE_ENV=production node app
```

### Plugins

Dillinger is currently extended with the following plugins

* Dropbox
* Github
* Google Drive
* OneDrive

Readmes, how to use them in your own application can be found here:

* [plugins/dropbox/README.md] [PlDb]
* [plugins/github/README.md] [PlGh]
* [plugins/googledrive/README.md] [PlGd]
* [plugins/onedrive/README.md] [PlOd]

### Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantanously see your updates!

Open your favorite Terminal and run these commands.

First Tab:
```sh
$ node app
```

Second Tab:
```sh
$ gulp watch
```

(optional) Third:
```sh
$ karma start
```

### Todos

 - Write Tests
 - Rethink Github Save
 - Add Code Comments
 - Add Night Mode

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [@thomasfuchs]: <http://twitter.com/thomasfuchs>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [marked]: <https://github.com/chjj/marked>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [keymaster.js]: <https://github.com/madrobby/keymaster>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>
   
   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]:  <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>


