# Mongo Java UUID Converter

Tool to convert Mongo BinData format to Java UUIDs and vice-versa. 
It behaves like the Java Mongo Driver which transmits the bytes of the [most and least significant bits in little endian format](https://jira.mongodb.org/browse/JAVA-403).

[I used this snippet from the Mongo C# Driver as reference](https://github.com/mongodb/mongo-csharp-driver/blob/master/uuidhelpers.js).
I added some comments to explain the bitwise operations if you want to take a look into the source code.

## Prerequisites

Python 3.8 installed.

## Installation

### For End-User

Use [Pipx to download and install the application in a virtual environment](https://github.com/pypa/pipx) or do it yourself with Pip and [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/install.html):

```bash
# use either pipx
pipx install --pip-args=--pre mongojuuid==0.1.1

# or alternatively pip 
python3 -m pip install --pre mongojuuid==0.1.1
```

# Usage

## CLI

The python installation ships with an executable named `mongojuuid`.
Alternatively use `python3 -m mongojuuid`

### Convert to Java UUID

```bash
>mongojuuid to-uuid 'BinData(3, "gJZnXl0vT+OXdGUUfuRraQ==")'
e34f2f5d-5e67-9680-696b-e47e14657497
```

### Convert to BinData

```bash
>mongojuuid to-bindata e34f2f5d-5e67-9680-696b-e47e14657497
BinData(3, "gJZnXl0vT+OXdGUUfuRraQ==")
```