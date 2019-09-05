# pymailer
A python utility to send mail from gmail using OAuth2.0

#### To download [click_here](https://raw.githubusercontent.com/abhishm20/pymailer/master/pymailer.zip)

### Setup
1. goto **downloads** directory where pymailer is downloaded
```bash
# e.g. cd ~/Downloads/
```
2. move **pymailer** to **home** directory
```bash
mv pymailer* ~/
```
3. set **alias** to execute as command
```bash
printf "alias pymailer='python ~/pymailer/pymailer.py'\n" >> ~/.bash_profile
```
4. load changes
```bash
source ~/.bash_profile
```
5. run setup
```bash
pymailer --setup
```
6. test sending a mail
```bash
pymailer -e your_email@gmail.com -s subject -b body
```

### Required libs
1. to install **httplib2**
```bash
pip install --upgrade httplib2
```
2. to install **oauth2client**
```bash
pip install --upgrade oauth2client
```
3. to install **google-api-python-client**
```bash
pip install --upgrade google-api-python-client
```

### Thanks