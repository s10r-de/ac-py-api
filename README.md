# Active Collab Python CLient

An API client, written in python to access Active Collab via the HTTP-API.

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

## Usage

### 1. Export data from cloud

Create a new `config*.ini` file from `config-example.ini`. You need to
provide your credentials to log in into Active Collab Cloud or
self-hosted and for the Cloud Login you also need to give the account
number (get it from URL).

Example `config-cloud.ini`:

```ini
[DEFAULT]
base_url = https://activecollab.com
is_cloud = 1

[LOGIN]
# best is to create a dedicated user account just for the
# API use, then you can add it only to the projects where
# you need it and limit therefore the access!
username = ac-api-test@example.com
password = ***secret***

# take the account number from the first segment of the URL
# this is only required for Cloud hosted Active-Collab, for
# self hosted it is ignored.
account = #123456

Then test if execution will work by print the version number:

```console
./acdump.sh -c config-cloud.ini info
{
    "application": "ActiveCollab",
    "version": "7.4.698",
    "is_cloud": true
}
```

Example to access a self-hosted instance:

```
```
[DEFAULT]
base_url = http://collab.example.com:8008/
dump_timestamp = /tmp/dump.txt
is_cloud = 0

[LOGIN]
username = ac@example.com
password = 12345678

[STORAGE]
path = ./self-hosted-data
```

## API Documentation

We only have the following information regarding our API:

We have resources available regarding our API - first the documentation page: <https://developers.activecollab.com/api-documentation/index.html>

The second is the GitHub repo with examples here: <https://github.com/activecollab/activecollab-feather-sdk>

And the third and most valuable one is the Stack-Overflow here: <https://stackoverflow.com/questions/tagged/activecollab>

If you need some further assistance on this, I encourage you to post all the questions about the API on Stack Overflow so that our developers can take a look and answer.

You can find [ER-Diagram](AcObjects.md)

## API Problems

- no paging: <https://github.com/activecollab/activecollab-feather-sdk/issues/29> (mostly)
  - <https://stackoverflow.com/questions/40020003/get-pagination-results-in-active-collab-api/40020858#40020858>
- no filter: <https://github.com/activecollab/activecollab-feather-sdk/issues/36>

## License

Use it like it is.  NO WARRANTY!  Be careful when accessing your production account!

