# DaViEx

### Follow the steps in order to run the project



## 1st step, clone the repository

```bash
git clone https://github.com/Devilmoon/DaViEx/
cd repo
```


## 2nd step, download dependecies:

Dependecies: Python 3.x, Plotly

```pip
pip install dash
pip install dash-html-components
pip install dash-core-components
pip install dash-table
```

## 3rd step, run the servers

First open four different terminals in the project root directory and run in three of them

```
python app1.py
python best.py
python worst.py
```

then in the last terminal, always in the root directory of the project run

```
set FLASK_APP=server.py 
flask run
```
