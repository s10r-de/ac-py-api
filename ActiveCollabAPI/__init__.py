AC_API_VERSION: int = 1

AC_API_CLIENT_NAME: str = 'backup-activecollab-py'
AC_API_CLIENT_VENDOR: str = 'ACME-VC'

AC_USER_AGENT: str = 'Active Collab Backup'

# because "class" is a reserved keyword in python we need to
# convert it to something else "class_" and back
AC_PROPERTY_CLASS = "class"
AC_PROPERTY_CLASS_ = "class_"

# Most AC Objects have a class name
AC_CLASS_ATTACHMENT_WAREHOUSE = "WarehouseAttachment"
AC_CLASS_COMMENT = "Comment"
AC_CLASS_COMPANY = "Company"
AC_CLASS_PROJECT = "Project"
AC_CLASS_PROJECT_CATEGORY = "ProjectCategory"
AC_CLASS_PROJECT_LABEL = "ProjectLabel"
AC_CLASS_PROJECT_NOTE = "Note"
AC_CLASS_SUBTASK = "Subtask"
AC_CLASS_TASK = "Task"
AC_CLASS_TASK_LABEL = "TaskLabel"
AC_CLASS_TASK_LIST = "TaskList"
AC_CLASS_USER_MEMBER = "Member"
AC_CLASS_USER_OWNER = "Owner"

AC_ERROR_WRONG_CLASS = "Wrong Object Class!"
