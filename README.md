# Where are my Sheep
  Research projects in collaboration with biologists and farmers look at automatically detecting sheep from aerial imagery, in particular multi-spectral images.  This can also applied to other animals such as deer.  This project looks into using these images to detect and count sheep.  A variety of methods can be explored.

## Installation

Uses a pip virtual enviroment, for ease of installing dependencies.
```
pipenv install
```

## Usage
Run code inside the pipenv using `pipenv run <cmd>` or `pipienv shell` 

See `main.py` for usage examples of the Image Manager and finders programmatically.

or

Run `python3 server/server.py` to run a flask server for interactive experience.

## Structure

`docs` contains any documentation related to the project

`tests` contains tests for the different modules

`server` contains server related code

`results` contains scripts used to produce results and analysis for the report

`finders` in hear you will find implementations to locate sheep.

`model` contains any models used, such as Location to store found sheep data.

`imageManager.py` contains the code for loading and saving the images and running the finders.

`main.py` example usages of the imageManger and finders

`pipfile` contains list of dependencies, used for the pipenv


