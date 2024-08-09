# Backup Active Collab

A tool to dump and later import Active Collab data over JSON Files.

Concept can be found in
Confluence: https://[example].atlassian.net/wiki/x/AYBXBw

## Setup

Requires Macbook with [Homebrew](https://brew.sh) installed.

Install the **python3.12** via homebrew, the build-in python3 will not
work because the urllib3 does not work with SSL!

```console
brew install python3@3.12
```

We are using [PyCharms IDE](https://www.jetbrains.com/pycharm/) for
development.

The project setup is already done for it.

## Running

Create a `config.ini` file from `config-example.ini`. You need to
provide your credentials to login and give the account number.

```ini
[LOGIN]
username = you@example.com
password = very-secret
account_name = #123456
```

Then test if execution will work by print the version number:

```console
AcDump/main.py -c config.ini -v 
{"version": "0.1"}
```

The script will currently always print JSON output.

## License

Only for internal use!  No public distribution!

_(c) 2024 by ACME VC GmbH, Charlie Sloan <cs@example.com>_
