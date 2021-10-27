TODO list:
    1) The model return the same answer for all inputs, possibly problem saving and reconstructing the model correctly
    2) There is no catching of Timeout errors, should fail gracefully
    3) Building the model outputs to the screen, that should be captured for debug output

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
