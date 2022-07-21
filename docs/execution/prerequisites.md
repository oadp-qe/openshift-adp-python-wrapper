# Prerequisites

## Environment prerequisites

The tests assume that
* the OADP operator is already installed on your cluster,
* you have an object storage available for the backup location
* you have a credentials file located on the machine where you execute the tests with the necessary permissions for the object storage operations and native snapshot operations in case it's applicable.

## Python prerequisites

Create virtualenv and install the modules from listed in the requirements:

```bash
PYTHON_BINARY=${PYTHON_BINARY:-python}
$PYTHON_BINARY -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install -Ur requirements.txt
```
