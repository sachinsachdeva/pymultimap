# pymultimap

[![PyPI - Version](https://img.shields.io/pypi/v/pymultimap.svg)](https://pypi.org/project/pymultimap)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymultimap.svg)](https://pypi.org/project/pymultimap)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install pymultimap
```

## Usage

```python
from pymultimap.multimap import MultiMap

mm = MultiMap()
mm["a"] = 1
mm["a"] = 2
mm["b"] = 3

print(mm)

```

```console
Should print :
{a: [1, 2], b: [3]}
```

## License

`pymultimap` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
