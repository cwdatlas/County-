---
County+ database search CLI
---
The county+ application is a continuation of the CountyDatabase github repo: https://github.com/cwdatlas/CountyDatabase.
This Database is accessed using a command then arguments delimited by spaces.

---
how to install
---
you must have git and python installed to run this program

- in a new folder use 'git repo clone 'https://github.com/cwdatlas/County-' in your command line
- To install packages type 'pip install -r requirements.txt'. You must be in the top level directory of the project. 
  - If you are having trouble using this command make sure you have pip installed and requirements.txt is in your current dir.
- Now, navigate to the 'src' directory, then type either python/python3/py main.py
  - The command you use depends on your system. 'py' worked for me.
- The application should boot up, if there is an error on boot that says "File not found in path" make sure the CountyRepo.csv is in the resources dir.

---
how to use
---
The commands in this program were inspired by the structure of linux type commands. 
There are 4 commands avaliable:
- add 'city name' 'county name'
  - when adding a city, your city must be unique and your stated county must exist.
  - example: 'add toston broadwater'
- get 'city/county/code' name
  - when getting a city, county or code you will need to specify which object type you wish to search.
  - The object must exist and there are no spaces in any city names or county names.
  - example: 'get city toston' or 'get county luis&clark'
- help
  - Provides help similar to what is seen here
- quit
  - safes quits the program