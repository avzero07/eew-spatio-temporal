# eew-spatio-temporal

## Dependencies

- obspy >=1.2.2
  - Install from the master branch of this fork : https://github.com/avzero07/obspy
  - Newer versions of obspy from source ought to be fine as well. Just make sure all tests pass.

- pytorch >=1.8.1 (cu102)
  - Install via pip

- pytest >=6.2.2
  - Tests are in pytest

TODO: Create a Poetry File to package project

## Setup

Once the dependencies are met, from the project root run pip install. I 
personally like editable installs but this is a personal preference.

```
eew-spatio-temporal$ pip install -e .
```

This will install est_lib. Refer to the test files to get a feel for
usage.

## Tests

At this time, tests are basic and are more to confirm that things run.
All tests should be passing. If not, something is wrong.

To run tests, after Setup, call pytest

```
eew-spatio-temporal$ pytest test/
```
