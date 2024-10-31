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

### Set up the Virtual Env

Create virtual environment and install the required modules:

```console
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt 
```

Always run it inside this venv!


## Running

Create a `config.ini` file from `config-example.ini`. You need to
provide your credentials to log in and give the account number.

```ini
[LOGIN]
username = you@example.com
password = very-secret
account_name = #123456
```

Then test if execution will work by print the version number:

```console
./acdump.sh -c config-test.ini version
{"version": "0.1"}
```

Get the servers version number:

```console
./acdump.sh -c config-test.ini info
{
    "application": "ActiveCollab",
    "version": "7.4.613"
}
```

The script will currently always print JSON output.

Trigger the dump of all data:

```console
./acdump.sh -c config-test.ini dump
{
    "message": "data of account 416910 dumped to ./data"
}
```


## Noteable

- **⚠️Limitation: completed projects and related data will _NOT_ be
  dumped!!**
- **⚠️Current implementation will always erase current data and create
  from scratch, this will change in a future version!!**
- This script will only backup the data where it has access to, remember when configure the account to give enough permissions!
- this script will not backup trashed projects or tasks or anything else
  what is trashed, but it will include completed projects tasks etc.!

To run the local self-hosted Active-Collab please read
the [Server Setup Page](./ActiveCollabServer/docs/Setup.md)

## API Documentation

We only have the following information regarding our API:

We have resources available regarding our API - first the documentation page: https://developers.activecollab.com/api-documentation/index.html

The second is the GitHub repo with examples here: https://github.com/activecollab/activecollab-feather-sdk

And the third and most valuable one is the StackOverflow here: https://stackoverflow.com/questions/tagged/activecollab

If you need some further assistance on this, I encourage you to post all the questions about the API on Stack Overflow so that our developers can take a look and answer.

You can find [ER-Diagram](AcObjects.md)

## API Problems

- no paging: https://github.com/activecollab/activecollab-feather-sdk/issues/29
  - https://stackoverflow.com/questions/40020003/get-pagination-results-in-active-collab-api/40020858#40020858
- no filter: https://github.com/activecollab/activecollab-feather-sdk/issues/36

## License

Only for internal use!  No public distribution!

_(c) 2024 by ACME VC GmbH, Charlie Sloan <cs@example.com>_
