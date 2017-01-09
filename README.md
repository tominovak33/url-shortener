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

    ### Use deploy script
    
    To deploy a new version with a generated name
    
    `./bin/deploy`
    
    Or to specify a custom name for the version
      
    `./bin/deploy name-here` 
   
    Warning: This will overrite the previous version with same, so use carefully  
    
    appcfg.py -A [YOUR_PROJECT_ID] update ./app

## Running locally


### Running the site locally

    ###### Basic run script

        dev_appserver.py ./app

    ###### Clear Datastore and run

        dev_appserver.py --clear_datastore=yes ./app

    ###### Only show warnings and erros, not standard logs

        dev_appserver.py --dev_appserver_log_level=warning ./app

    ###### Set the datastore to be persistent locally (otherwise it goes in the tmp folder)

        dev_appserver.py --storage_path ./.datastore ./app

    ###### While developing I suggest using this combination of the above commands

        dev_appserver.py --clear_datastore=yes --dev_appserver_log_level=warning ./app

    ###### To access the site from different host

        dev_appserver.py ./app --host 0.0.0.0

  * Browse to the site on your chosen equivalent of [http://localhost:8080](http://localhost:8080).
