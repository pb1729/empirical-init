# Notes on Testing and Building

Terminology: "repo root directory" refers to the primary directory of the repo, aka the same directory that this file is in.

## Building the package

From the repo root directory, run:

```
python -m build
```
d 
## Testing the package

First we make sure that the version of empirical init we want to test is installed. To do this, we run the following from the repo root directory:

```
pip install --upgrade .
```

Then to run the tests:

```
python tests/test_ei.py
```


## Uploading the package

Test upload (note the we use wildcard so that we can just paste without knowing the versioon number):

```
python -m twine upload -r testpypi dist/empirical_init-*.tar.gz
```

Full PyPI upload:

```
python -m twine upload dist/empirical_init-*.tar.gz
```


## References
* https://realpython.com/pypi-publish-python-package/
* https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

