# ActiveCollab Python CLient

An API client, written in python to access ActiveCollab via the HTTP-API.

## Setup

Requires Linux or a Macbook with Docker and [Homebrew](https://brew.sh) installed.

On the Mac install the **python3.13** via Homebrew, the build-in python3 will
not work because the `urllib3` does not work with SSL!

```console
brew install python3@3.13
```

### Set up the virtual environment

Create a python virtual environment and install the required modules:

```console
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt 
```

Always run the script it inside this virtual environment!

Check main:

```
PYTHONPATH=$PWD:$PYTHONPATH python3 active_collab_app/main.py --help
```

## Usage

### 1. Connect

Create a new `config*.ini` file from `config-example.ini`. You need to
provide your credentials to log in into ActiveCollab Cloud or
to your self-hosted instance. For the Cloud Login you also need to 
give the account number (get it from URL).

Example `config-localhost.ini`:

```ini
[DEFAULT]
#base_url = https://activecollab.com
#is_cloud = 1
base_url = http://localhost:8008
is_cloud = 0

[LOGIN]
username = you@example.com
password = very-secret
#account = #123456
```

Then test if execution will work by print the version number:

```console
$ PYTHONPATH=$PWD:$PYTHONPATH python3 active_collab_app/main.py --config config-localhost.ini  info
{
    "application": "ActiveCollab",
    "version": "7.4.375",
    "is_cloud": false
}
```

## Official API Documentation


- The documentation page: <https://developers.activecollab.com/api-documentation/index.html>
- GitHub repo with examples here: <https://github.com/activecollab/activecollab-feather-sdk>
- Stack-Overflow here: <https://stackoverflow.com/questions/tagged/activecollab>

If you need some further assistance on this, I encourage you to post all the questions about the API on Stack Overflow so that our developers can take a look and answer.

You can find [ER-Diagram](AcObjects.md)

### API Problems

- no paging: <https://github.com/activecollab/activecollab-feather-sdk/issues/29> (mostly)
  - <https://stackoverflow.com/questions/40020003/get-pagination-results-in-active-collab-api/40020858#40020858>
- no filter: <https://github.com/activecollab/activecollab-feather-sdk/issues/36>


