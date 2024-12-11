
## Example Export and Import to Backup-System

Login to the Backup-System and change owner to be the "activecollab" User.

```
% ssh cs@mira-backup1.[example].de
% ./activecollab.sh
```

### Create a new dump

Run:

```
% cd /srv/activecollab/active-collab-backup
% ./acdump.sh -c ../config-cloud.ini --debug dump
{
    "account": 416910,
    "storage_path": "../cloud-data",
    "statistics": {
        "attachments": 2849,
        "companies": 1,
        "project_categories": 1,
        "project_labels": 11,
        "project_notes": 11,
        "projects": 75,
        "subtasks": 2763,
        "task_comments": 8610,
        "task_history": 12981,
        "task_labels": 12,
        "task_lists": 481,
        "tasks": 1712,
        "users": 52
    }
}
INFO - Finished after 1942.760 seconds
```


### Delete previous data

Mark all items as deleted (move to trash):

```
% cd /srv/activecollab/active-collab-backup
% ./acdump.sh -c config-selfhosted.ini --debug delete
true
INFO - Finished after 198.733 seconds
```

Now empty the trash-bin:

```
% cd /srv/activecollab/active-collab-backup
% ./acdump.sh -c config-selfhosted.ini --debug empty
# shows item list from trash bin, if any existing
INFO - Finished after 47.668 seconds
```

Because not all data is deleted some tables need to be manually truncated.  Open the [Adminer Webinterface](https://ac-backup.[example].de:8443/?server=db&username=root&db=acdb&sql=) to get access to the database and run this SQL:

```sql
use acdb;

truncate access_logs;
truncate activity_logs;
truncate email_log;
truncate jobs_queue;
truncate jobs_queue_failed;
truncate messages;
truncate modification_logs;
truncate modification_log_values;
truncate security_logs;
truncate uploaded_files;
truncate user_sessions;
```

### Import the dumped data

Run it and save the logfile.

```
% cd /srv/activecollab/active-collab-backup
% ./acdump.sh -c config-selfhosted.ini --debug load > load.log 2>&1
{
    "all": {
        "attachments": 2849,
        "companies": 1,
        "project_categories": 1,
        "project_labels": 11,
        "project_notes": 0,
        "projects": 75,
        "subtasks": 2763,
        "task_comments": 8610,
        "task_history": 0,
        "task_labels": 0,
        "task_lists": 481,
        "tasks": 1712,
        "users": 52
    },
    "success": {
        "attachments": 2812,
        "companies": 0,
        "project_categories": 1,
        "project_labels": 11,
        "project_notes": 0,
        "projects": 75,
        "subtasks": 2763,
        "task_comments": 8610,
        "task_history": 0,
        "task_labels": 0,
        "task_lists": 481,
        "tasks": 1712,
        "users": 52
    },
    "completed": {
        "attachments": 0,
        "companies": 0,
        "project_categories": 0,
        "project_labels": 0,
        "project_notes": 0,
        "projects": 1,
        "subtasks": 2520,
        "task_comments": 0,
        "task_history": 0,
        "task_labels": 0,
        "task_lists": 57,
        "tasks": 1121,
        "users": 2
    }
}
INFO - Finished after 4062.518 seconds
```

### Verify the import

```
% ./acdump.sh -c config-selfhosted.ini --debug verify > verify.log 2>&1

```


## Login to the Backup-System

After all was working without problems the users can login to the Backup-System:

[https://ac-backup.[example].de/](https://ac-backup.[example].de/)

> Note: When import data the users will get a new random password.  You will find the password in the output of the "load" command!  run `grep "password for user" load.log`

Owner Account is "ac-dump@example.com".  Password see Bitwarden.

> Note 2: By default are no Cronjobs enabled.  How to enable read the other docs.

> Note 3: The Backup-System is configured to send emails to the self-hosted "[Mailcow](https://ac-backup-mail.[example].de)" Mailserver.  Access is possible via [Web-Mail](https://ac-backup-mail.[example].de/SOGo/). This means the emails will be **not** delivered to any real email box.

More technical information can be found in the GIT Repositories:

- https://bitbucket.org/[example]/active-collab-server
- https://bitbucket.org/[example]/active-collab-backup
- https://bitbucket.org/[example]/active-collab
