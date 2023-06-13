# Find API Key

![Generic badge](https://img.shields.io/badge/python-3.8-blue.svg)

This script scans a directory and identifies files that reference an API key.  By default, the script searches for matches that contain a key named 'api_key'. However, a custom key name can be specified as an argument.

## Prerequisites

Python 3.8 or higher

## Installation

1. Clone the repository:

```text
git clone https://github.com/dfirsec/find_api_key.git
```

## Usage

1. Navigate to the project directory:

```text
cd find_api_key
```

2. Run using the following commands:

```text
python find_api_key.py /path/to/directory
```

To specify a custom key name for the script to search for, use the -a or --api flag followed by the key name:

```text
python find_api_key.py /path/to/directory --api custom_key
```

### Example

```text
python find_api_key.py /path/to/directory
```

This will scan the specified directory for API key references in files and display the results. The results will contain the file path, the line number where the API key references was found, and the actual API key.

```text
python find_api_key.py /path/to/directory --api custom_key
```

This will scan the specified directory for custom key name references in files and display the results.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.
