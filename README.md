# Artickle-Manager
This project is a scientific article manager that allows you to save links to articles with categories (Uninteresting categories can be disabled in the base_config.json configuration file) of interest to you in a database (Currently only habr.com is supported)
In the future, it is planned to add support for most other sites, as well as add GUI and data statistics.

# Installation
1. Install all dependencies from requirements.txt
2. This repository works with postgresql, you need to fill in the .env file according to the .env.exmaple pattern
3. Run the file run.py

# Remarks
The csv file is saved in the data folder, the Power BI dashboard is also located there, you can specify the path to this file in this dashboard and get information on the articles that have been added since the last launch of the program
The article to which you need to search lies in the raw data folder in txt format, just specify the link and all articles published after it will be worked out and entered into the database
