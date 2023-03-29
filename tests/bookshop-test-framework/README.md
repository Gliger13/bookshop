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
5) Install test framework dependencies using [requirements.txt](requirements.txt):
```shell
pip install --requirement --no-deps requirement.txt
```
6) Install test framework [pyproject.toml](pyproject.toml):
```shell
pip install --no-deps .
```
_Note: To install dev version for contributing please use
`pip install --requirement --no-deps dev-requirement.txt` and then
`pip install --no-deps ".[dev]"`_
