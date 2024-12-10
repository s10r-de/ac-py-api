# Backup Active Collab

A tool to dump and later import Active Collab data over JSON Files.

Concept can be found in
Confluence: <https://[example].atlassian.net/wiki/x/AYBXBw>

## Setup

Requires Linux or a Macbook with Docker and [Homebrew](https://brew.sh) installed.

On the Mac install the **python3.12** via homebrew, the build-in python3
will not
work because the urllib3 does not work with SSL!

```console
brew install python3@3.12
```

Checkout from Bitbucket:

```console
git clone git@[repo]/active-collab-backup.git
```

We are using [PyCharms IDE](https://www.jetbrains.com/pycharm/) for
development. The project setup is already done for it.

### Set up the Virtual Env

Create a python virtual environment and install the required modules:

```console
cd active-collab-backup
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt 
```

Always run the script it inside this venv!

## Usage

### 1. Export data from cloud

Create a new `config*.ini` file from `config-example.ini`. You need to
provide your credentials to log in into Active-Collab Cloud or
self-hosted and for the Cloud Login you also need to give the account
number (get it from URL).

Example config-cloud.ini:

```ini
[DEFAULT]
base_url = https://activecollab.com
is_cloud = 1

[LOGIN]
username = ac-api-test@example.com
password = ***secret***
account = #123456

[STORAGE]
path = ./data-cloud
```

Then test if execution will work by print the version number:

```console
./acdump.sh -c config-cloud.ini info
{
    "application": "ActiveCollab",
    "version": "7.4.698",
    "is_cloud": true
}
```

Now you can start the dump of all data:

```console
./acdump.sh -c config-cloud.ini dump
{
    "message": "data of account 416910 dumped to ./data-cloud"
}
```

All data will be saved under `./data-cloud` (see config file "
STORAGE.path") and previous data in this folder will be removed!

## Noteable

- ⚠️ Warning: The current implementation will always erase the existing
  data in the `storage.path` directory on disk and re-download everything
  from scratch!
- ⚠️ Limitation: Completed projects, tasks, and related data will not be
  deleted or backed up!
- This script will not back up any trashed projects, tasks, or other
  items. However, it will include completed projects, tasks, and other
  related data.
- This script will only back up data for which the configured user has
  permission. Make sure to grant sufficient permissions when setting up
  the account

### 2. Import to self-hosted Active Collab

To run the local self-hosted Active-Collab please follow the setup
instructions described in
the [active-collab-server](https://bitbucket.org/[example]/active-collab-server/src/main/)
repository.

Create another config file for the self-hosted server (here we run it in
a linux VM under IP 192.168.64.14):

Example `config-selfhosted.ini` (use credentials you have used to setup
the self-hosted ac owner):

```ini
[DEFAULT]
base_url = http://192.168.64.14:8008
is_cloud = 0

# map company id 5 to 1
map_company_id_5 = 1

[LOGIN]
username = ac-dump@example.com
password = 1234567890
account = 0

[STORAGE]
path = ./data-selfhosted
```

Test if the connection works:

```console
./acdump.sh -c config-selfhosted.ini info
{
    "application": "ActiveCollab",
    "version": "7.4.375",
    "is_cloud": false
}
```

Copy the data dumped from cloud to the self-hosted storage directory

```console
mkdir data-selfhosted
cp -r data-cloud/account-00416910 data-selfhosted/account-00000000
```

Now import all the data:

```console
./acdump.sh -c config-selfhosted.ini --debug load
```

The script should not be interrupted. If it stops for some reason you
need to start from scratch by first empty the database and then import
all data again.

```console
# delete all data (move to trash)
# **BE CAREFUL TO USE THE RIGHT CONFIG**

./acdump.sh -c config-selfhosted.ini --debug delete

# finally empty the trash

./acdump.sh -c config-selfhosted.ini --debug empty
```

Note: depending on how much you have already used the self-hosted server
it may be required to empty the cache folder in the docker container:

```console
docker exec -it active-collab-server-active-collab-server-1 bash
rm -fr /var/www/html/cache/*
```

### 3. Make self-hosted productive

#### Automatic tasks (cron)

The CRON jobs are not starting automatically because you should do some
manual configuration before starting them!

You should run the CRON jobs manually once, before configure email
server or push notification service. This will generate all email and
push notifications inside the database table `job_queue`.

Note: The import of the data will generate new notifications for each
project/task/subtaks/comment/attachment added.

You should then remove all the notifications from database. Use "
adminer" and login into the database with the "acuser" credentials.

Then cleanup the table

```sql
delete * from job_queue;
```

You can find the CRONTAB here:

```console
cat /root/activecollab-crontab 
* * * * * /usr/bin/php '/var/www/html/tasks/cron_jobs/run_every_minute.php'
#*/3 * * * * /usr/bin/php '/var/www/html/tasks/cron_jobs/check_imap_every_3_minutes.php'
#0 * * * * /usr/bin/php '/var/www/html/tasks/cron_jobs/run_every_hour.php'
* 
```

### Configure Email Notifications

After you have cleaned up the job-queue you can configure the Email
Server and Push notification server. This is done by login to AC with
the Owner Account and go to System-Settings (see original documentation
by the vendor ov AC).

## API Documentation

We only have the following information regarding our API:

We have resources available regarding our API - first the documentation page: <https://developers.activecollab.com/api-documentation/index.html>

The second is the GitHub repo with examples here: <https://github.com/activecollab/activecollab-feather-sdk>

And the third and most valuable one is the StackOverflow here: <https://stackoverflow.com/questions/tagged/activecollab>

If you need some further assistance on this, I encourage you to post all the questions about the API on Stack Overflow so that our developers can take a look and answer.

You can find [ER-Diagram](AcObjects.md)

## API Problems

- no paging: <https://github.com/activecollab/activecollab-feather-sdk/issues/29>
  - <https://stackoverflow.com/questions/40020003/get-pagination-results-in-active-collab-api/40020858#40020858>
- no filter: <https://github.com/activecollab/activecollab-feather-sdk/issues/36>

## License

Only for internal use!  No public distribution!

_(c) 2024 by ACME VC GmbH, Charlie Sloan <cs@example.com>_
