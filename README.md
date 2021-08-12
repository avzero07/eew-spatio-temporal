# `est_lib` An API for Acquiring and Interacting with Seismic Data

## Setup

### Dependencies

- Python >= 3.8
- obspy >=1.2.2
- pytorch >=1.8.1 (cu102)
- pytest >=6.2.2
- jupyter (or any other IPython notebook viewer)

Latest versions of all these dependencies should work fine. They may be installed using
pip or whatever package management tool you might be using. If in doubt, use pip.

### Installation

Once the dependencies are met, from the project root run pip install. I 
personally like editable installs but this is a personal preference.

```
eew-spatio-temporal$ pip install -e .
```

This will install `est_lib`. Refer to the IPython notebooks in the `workflow_demos` folder
for a tutorial on how `est_lib` might be used.

## Tests

All tests are written in Pytest. After installing dependencies, call pytest from the project
root to run all tests. All tests should be passing and you should see an output similar to
the snippet pasted below. In case of errors please confirm whether all dependencies are
set up correct.

If problems still persist, please open an issue on this repository so that I can advise.

```
eew-spatio-temporal$ pytest
================================================= test session starts =================================================
platform win32 -- Python 3.8.8, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: C:\Users\aksha\Desktop\eew-spatio-temporal
collected 51 items

tests\test_dataset.py ........                                                                                   [ 15%]
tests\test_event_parse.py ...............                                                                        [ 45%]
tests\test_init.py .                                                                                             [ 47%]
tests\test_nn.py ..........                                                                                      [ 66%]
tests\test_nn_common.py ....                                                                                     [ 74%]
tests\test_util.py .............                                                                                 [100%]

================================================= 51 passed in 22.27s =================================================
```


