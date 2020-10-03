# NBATwitterCorrelation
This project aims to determine if there is any correlation between
 an NBA player's performance and their pregame tweets.

## Developers:

#### PyCharm Development
When using the PyCharm IDE, before you do anything, open the terminal
in PyCharm. In the terminal, enter ```pyb pycharm_generate```. 
This will set up the environment so PyCharm knows how to interpret
the project.

#### Required Libraries
All required libraries will be located in requirements.txt and
requirements.in. These two files will be automatically maintained
using pip-tools. Use the command ```pip3 freeze > requirements.in```
to receive all the libraries used for THIS project's Python interpreter/venv.
It is key that this project has it's own interpreter/venv for this to work.
Then, requirements.txt can be generated using ```pip-compile```.

#### Structure
All python source code should be located under the ```src/main/python``` directory. 
If multiple files work together to perform one main task they should be placed
under a new subdirectory. For example, if I group of files is used to retrieve
data, they should go under a directory name data_retrieval.
The scripts directory will be used to contain the runnable scripts 
for our program. 

Do not worry about the unittest package for now. If in the
future we decide to include testing, we will discuss it then because
pybuilder requires a certain structure and specific file naming techniques.
