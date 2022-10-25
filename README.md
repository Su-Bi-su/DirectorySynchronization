# DirectorySynchronization
Synchronizes the files and sub-directories between two directories.
However, it is only a one way synchronization.

## Installation#

The main program only uses the python built-in libraries.

For unit-testing PyTest is used:
Installation is as follow:

```
pip install pytest
```

```
pip install pytest-dependency
```


## Usage
1. Clone the repository or download the repository

2. Using command line navigate to the "src" directory

### For unit testing

```
pytest -v
```

### For running the program

- Arguments can be provided using command line

Arguments : "source directory", "replica directory", "synchronization interval" , "log file" , and "timeout"

- "source directory" and "replica directory" are mandatory arguments
- "synchronization interval" , "log file" , and "timeout" are optional arguments
- Default values : 
-       - synchronization interval = 5sec , 
        - log file" = src\synclog.log , and 
        - timeout = 0(for continuous synchronization, without timeout)

```
python sync_directories.py "<source directory>" "<replica directory>"
```

OR

```
python sync_directories.py "<source directory>" "<replica directory>" -i <schedule interval> -l <logfile> -t <timeout>
```


- This program can also be used to run in background in windows machine using Task Scheduler


