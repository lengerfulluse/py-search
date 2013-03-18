---
layout: post
category: work
tags: {python, language}
---

{% JB/Setup %}

###HOW TO py-search###
implemented by python to create an integrated search engine module, including crawler, indexing&amp;search, web interface.
#### Main Three Modular ####
- index-creator from database.
- search modular with Whoosh
- web interface GUI with web.py template.
- kylin desktop search application. **Here, we supply the query results sorted function **

#### Source Directory #####
	
	.
	|-- **indexer_from_db.py**: creating index from database.
	|-- **searcher.py**: main search api.
	|-- web/
	|-- |--code.py: python servlet for web.py
	|-- templates/
	|-- |--index.html: web interface for user query input.
	|-- gui/
	|-- |--kylin-desktop.py: main desktop application.
	|-- |data-index/: index data files.
	|-- README.md
	|-- README.txt: same as above.
	|-- kylin-desktop.py: same as web directory
	|-- web-gui.py: same as code.py
	
#### Congiure & Install ####

- >1.	mysql-connector-python-1.0.9-py2.7.msi install
- >2.	install setuputils through ez_setup.py, and then add Script subdirectory in python install to env variables.
- >3.	install Whoosh 2.4.1 with the easy_install.exe tools
- >4.   install web.py with easy_install for web front end display.
- >5.   install xlwt package for write results to excel.