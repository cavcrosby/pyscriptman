# pyscriptman

# Brief

**pyscriptman** is a python application used to perform scripting actions on particular hosts.

## Installation

***Installs for the current user (or at the user level).***

```python
git clone https://github.com/reap2sow1/pyscriptman.git
python -m pip install requirements.txt
```
For desktops (or OSES with an DE):
```python
python installer.py --desktop
```

For servers (or OSES ***without*** an DE):
```python
python installer.py
```

To uninstall:
```python
python installer.py --uninstall
```



## NOTES

### Other Configurations
    - To use actions involving GitHub.com, an api_token will need to be generated and added to the etc/pyscriptman_configs.toml file.
    - To run the tests in 'test', configuration variables will need values in etc/test_configs.toml file.
