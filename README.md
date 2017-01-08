# Tomi URL Shortener

## Installation


* Install pip

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

    sudo python get-pip.py

* Google App Engine SDK for Python

    * Visit [App Engine SDK](https://cloud.google.com/appengine/downloads#Google_App_Engine_SDK_for_Python) and follow instructions for your OS

* Node.js & NPM

    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt-get install -y nodejs

* Gulp

    sudo npm install gulp -g



## Deploy

    appcfg.py -A [YOUR_PROJECT_ID] update ./app
