This program will classify either an single image or scrape 5 images from www.deviantart.com
Example:
	python3 webscraper.py -s dog

For full usage see help.txt

The program includes several files:

	webscraper.py
		- This is the main python file.
	
	help.txt
		- This file contains usage information
	
	dognames.json
		- This file contains dognames that match the model output.  This is used to
		assign breed name to the value returned by the model
	
	dog_model <directory>
		- This is the store information about the model used to make the predictions
