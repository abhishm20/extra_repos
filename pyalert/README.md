# pyalert
A python utility to send mail whenever error added to a log file


### Setup
1. install **pymailer**, visit [here](https://github.com/abhishm20/pymailer)

2. download **pyalert**, click [here](https://raw.githubusercontent.com/abhishm20/pyalert/master/pyalert.py)

3. change **email**
```python
TO_EMAIL = "your_email"
```
4. change **error log file path**
```python
ERROR_LOG_FILE = "/home/ubuntu/error.log"
```
5. change **app name**
```python
APP_NAME = "your app name"
```
6. change **time stamp format**
```python
TIME_STAMP_FORMAT = '[%d/%b/%Y %H:%M:%S]' # for [03/Apr/2017 23:01:32]
```