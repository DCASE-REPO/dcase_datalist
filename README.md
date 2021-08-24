DCASE Datalist
===============

This repository is a community effort of collecting meta-information about all DCASE related datasets into one place. Based on the metadata in this repository, tables in the [DCASE Datalist website](http://dcase.community/) are generated. 

This repository focuses specifically on pre-packaged **datasets** rather than online data repositories. A dataset should be well documented, packaged for easy usage, and have a free or open license for academic research. 

Instructions to add a new dataset to this list
----------------------------------------------

1. Fork this repository
2. Identify a category for the dataset: scenes, events, captions
3. Copy appropriate dataset template based on the category (e.g. `datasets\scenes_template.yaml`) from the root of `datasets\` to `datasets\scenes`, `datasets\sounds`, or `datasets\captions`, and rename the template accordingly  
4. Update information in the YAML file. Delete fields that are not needed. If you would like to have fields that do not yet exist, raise an issue in Github.   
5. Make a pull request from your fork to the main repository.

Optionally, you can raise an [issue](https://github.com/DCASE-REPO/dcase_datalist/issues) to this repository. 

Instructions to preview the dataset information
-----------------------------------------------

1. Run `update.py` to update `.json` files
2. Start the local server with `start_local_server.py`
3. Open URL http://localhost:8000/ 
