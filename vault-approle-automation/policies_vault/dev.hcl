{
  "path":{
    "secret/*":{"capabilities":["list"]},
    "secret/project_name/repo_name/env_name":{"capabilities":["read", "list", "update", "create", "delete"]},
    "secret/project_name/repo_name":{"capabilities":["read", "list", "update", "create", "delete"]},
    "secret/project_name":{"capabilities":["read", "list", "update", "create", "delete"]}
  }
}