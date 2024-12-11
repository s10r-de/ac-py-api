# Known Issues

## 1. "verify" shows different filesizes for attachments

this is under observation, no solution yet, but it seems attachments are all existing and workgin...


## 2. inline attachments are not inline

All inline attachments are shown as attachment and in the text a placeholder text is shown.  There is currently no soulution for this.

## 3. task history is not the old (original) history

There is no API to import the old history of a task, instead when inserting data the history will be updated.

There is currently no solution for this.

## 4. Missing objects

The listed data is not handled and therefore missing.  Please request a change to the "IT-Department" if you need this data in the backup system.

* Teams
* Peoples Avatar
* Project Templates
* Project Expenses
* Project Notes
* Bugets
* Discussions
* Task Estimates
* any Time Records
* anything related to Invoicing or Payment
* Reports & Filters

see https://app.activecollab.com/416910/projects/604/tasks/21955

## 4. Calendar is empty

The Calendar is updated by some background CRON Task.  By default the CRON on the Backup-System is disabled.  To enable the Calendar the CRON must be runninng, but this has also other effects, like sending notifications and emails etc.

See other documentation about enable CRON.

## 5. No Emails no Notifications

Emails and Notfications are send by some background CRON Task. By default the CRON on the Backup-System is disabled.  To enable the Notifications the CRON must be runninng, but this has also other effects, like sending notifications and emails etc.

See other documentation about enable CRON.  It also requieres the correct mail server setup and for push notifications an account at the [pusher](https://pusher.com) service.




