# FEMA Visualization

## Get Start

0. **(Do follow step ONLY if you build first time)**
	* install Node-js
	* `npm install -g grunt-cli`
	* goto website directory and type `npm install`
1. build and start server: `grunt server`
2. generate data
	* goto data-process directory
	* `python for-visual.py`
	* `python format-transform.py > graph.json`

If you need to deploy and don't need a temporal HTTP server:

* Type `grunt` instead to build all dependency.
* set a static HTTP server, the Root directory of which should be `website/dist`

## Thing to do before real deploy:

* Now the output of program `format-transform.py` has beautiful indent which enlarge the data file size
* uglify all css and js to decrease load time
