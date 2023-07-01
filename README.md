# Find API Key

![Generic badge](https://img.shields.io/badge/python-3.8-blue.svg)

This script scans a directory and identifies files that reference an API key.  By default, the script searches for matches that contain a key named 'api_key'. However, a custom key name can be specified as an argument.

## Prerequisites

Python 3.8 or higher

## Installation

Script utilizes standard Python libraries.

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

To specify a custom key name for the script to search for, use the --api flag followed by the key name:

```text
python find_api_key.py /path/to/directory --api "api-custom-key"
```

### Example

```text
python find_api_key.py /path/to/directory
```

This will scan the specified directory for API key references in files and display the results. The results will contain the file path, the line number where the API key references was found, and the actual API key.

```text
python find_api_key.py /path/to/directory --api "api-custom-key"
```

This will scan the specified directory for custom key name references in files and display the results:

> NOTE: The API key values below are bogus and were generated using [Generate Random](https://generate-random.org/).

```text
Searching for api_key references in files...

Files containing api_key references:
-----------------------------------
<DIRECTORY>\check_rep\settings.yml:
  Lines 2: ms5xxvszc0obohd0iu04axtyz8yb28ndn (User API Key)
<DIRECTORY>\general_scripts\abuseipdb.py"
  Line 20: ji4bh27m9chw1p2prica2qgmuhsyxqjfo4c30ntgxj0kx3w7s49gvq6fhvyvzt0v9rzwq4w17i61phnz (User API Key)
<DIRECTORY>\pythoncode\general\url_shortener.py:
  Line 5: qe8s4jydfc0o3zw1mo1u8okbl6pqiy94pqerg (User API Key)
<DIRECTORY>\shodan-scripts\androidcam\androidcam.py:
  Line 9: z719pelyjoa4nrs93mgsu01vnx97zhty (User API Key)
<DIRECTORY>\shodan-scripts\assets\assets.py:
  Line 14: z719pelyjoa4nrs93mgsu01vnx97zhty (User API Key)
<DIRECTORY>\shodan-scripts\cams\cams.py:
  Line 15: z719pelyjoa4nrs93mgsu01vnx97zhty (User API Key)
<DIRECTORY>\shodan-scripts\fos-streamer\fos.py:
  Line 15: z719pelyjoa4nrs93mgsu01vnx97zhty (User API Key)
<DIRECTORY>\shodan-scripts\IP Webcam\ipwebcam.py:
  Line 17: z719pelyjoa4nrs93mgsu01vnx97zhty (User API Key)
<DIRECTORY>\shodan-scripts\simplehttp\simple.py:
  Line 19: z719pelyjoa4nrs93mgsu01vnx97zhty (User API Key)
<DIRECTORY>\shodan-scripts\weblogic\weblogic.py:
  Line 62: z719pelyjoa4nrs93mgsu01vnx97zhty (User API Key)
```


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please create an issue or submit a pull request.

## License

This project is licensed under the MIT License.
