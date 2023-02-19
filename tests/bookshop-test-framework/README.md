# Bookshop Test Framework

## Installation

1) Switch to the `bookshop-test-framework` folder (guessing you are at the root repository level):
```shell
cd tests/bookshop-tests-framework
```
2) Create python virtual environment using python with version >= 3.11
```shell
python3.11 -m venv venv
```
3) Activate installed virtual environment
```shell
source venv/bin/activate
```
4) Install test framework and its base dependencies using [pyproject.toml](pyproject.toml):
```shell
pip install .
```
_Note: To install dev version with some code linters use `pip install ".[dev]"`_
