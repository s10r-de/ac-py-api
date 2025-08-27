# ActiveCollab Objects

All objects are stored under `Account`.

Many objects have a reference to related project_id.

```mermaid
erDiagram
    Company ||--o{ User: company_id
    Company ||--o{ Project: company_id
    Project }o--o{ User: members
    Project ||--o{ Task: project_id
    Project ||--o{ ProjectNote: project_id
    Project }o--o{ ProjectLabel: project_id
    ProjectNote o|--o{ Attachment: "parent_id+parent_type"
    Task }o--o{ TaskLabel: labels
    Task ||--o{ SubTask: task_id
    Task ||--o{ TaskHistory: task_id
    Task |o--o{ Attachment: "parent_id+parent_type"
    Task ||--o{ Comment: "parent_id+parent_type"
    Comment |o--o{ Attachment: "parent_id+parent_type"
```

You need a Markdown Viewer with "[Mermaid](https://mermaid.js.org/)" Plugin to see the diagram.
