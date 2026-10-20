# Local Credentials

Keep source code and non-secret configuration tracked. Keep credentials in
environment variables or ignored local files, never in source, examples, logs,
reports, or exported evidence.

- `JiraStoryCreater/secrets.local.json` stores local Confluence and VIRA PATs.
  Start with the empty `secrets.example.json` template. Environment variables
  `CONFLUENCE_PAT` and `VIRA_PAT` override local values.
- `.token_cache.json` and `.dtc_token_cache.json` are local Azure authentication
  caches. They are ignored and untracked; tools regenerate them through Azure
  CLI authentication when needed.
- `.env` variants, local secret JSON files, and private-key containers are
  ignored. Only credential-free example files should be committed.

## Previously Committed Credentials

Rotate the Confluence and VIRA PATs that appeared in earlier commits. Treat
previously committed Azure bearer tokens as exposed as well; revoke affected
sessions or credentials according to your organization's process if still valid.

Ignoring files and removing them from the current index does not remove their
contents from earlier commits, remote clones, or backups. This cleanup does not
rewrite history or force-push. A coordinated history purge, if required, must
also cover remote branches/tags and collaborators' clones after rotation.

Do not share restoration backups: they can contain the original credentials.