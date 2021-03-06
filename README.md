# Flask-Web self learning

* Clone the repo.
* Copy ```config.py.default``` to ```config.py``` .
* Change values in ```config.py``` as per requirements.
* Install npm packages ```npm install```.
* Install bower packages ```bower install```.
* Run ```./init.sh```.
* Create a virtualenv.
* Activate virtualenv.
* Do ```pip install -r requirements.txt```.
* Perform unittests if you want ```FLASK_CONFIG=test python manage.py test```.
* Create DB
    * ```python manage.py db init```
    * ```python manage.py db migrate```
    * ```python manage.py db update```
* Run gulp ```gulp clean && gulp```.
* Start dev server ```python manage.py runserver```.

## Issues
* Report issues or suggestions [here](https://github.com/brijeshb42/yapper/issues/new).
* Pull requests are welcome :thumbsup: .

## TODO

* Documentation of functionalities that have been added.
* New UI and functionality for adding blog post with tags, categories, description, slug and status(draft or published).
* Theming support (if possible).
