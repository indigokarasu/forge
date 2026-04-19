# Deferred: belongs in the ocas-auth private repo (https://github.com/indigokarasu/ocas-auth), not in ocas-forge. Content preserved here until that skill exists.

This content describes OAuth token management, Google API scope handling, and MCP server registration. That is authentication and service-wiring guidance — it belongs in a dedicated `ocas-auth` skill, not in the skill-builder. It was removed (and deduplicated) from `ocas-forge/SKILL.md` during the 2026-04 refactor. OAuth scope material appeared in three of the merged helper skills; the canonical treatment is consolidated below.

---

## Google OAuth integration

### Check existing token scopes

```bash
cat {agent_root}/google_token.json
```

The token file lives at `~/.hermes/google_token.json` on Hermes installs, or at `{agent_root}/google_token.json` generally.

### Scope handling

Google OAuth scopes must include **every** API the calling skill uses. The token must have scopes for Drive, Gmail, Calendar, Contacts, Sheets, and Docs as needed. If any required scope is missing, API calls to that service return 403.

**Common scope mismatches** between spec and token:
- Specification requests: `gmail.readonly`, `calendar.readonly`
- Token actually has: `gmail.modify`, `calendar`

**Solution**: use the scopes that match the existing token, not the ones the spec requested. When in doubt, re-issue the token with the union of required scopes rather than editing the skill.

**Debugging 403 errors**: when a skill that accesses Google services reports 403 errors, check the token scopes first — not the skill logic.

### Initialize Google services (Python)

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from pathlib import Path

token_path = Path.home() / ".hermes" / "google_token.json"

creds = Credentials.from_authorized_user_file(
    str(token_path),
    ['https://www.googleapis.com/auth/gmail.modify',
     'https://www.googleapis.com/auth/calendar']
)

def get_gmail_service():
    creds = Credentials.from_authorized_user_file(str(token_path))
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('gmail', 'v1', credentials=creds)
```

---

## MCP server configuration

### Register an MCP server with Hermes

```bash
hermes mcp add {server_name} --command npx --args @package/mcp-server --auth header
```

### MCP config file

Create `/root/.hermes/mcp/{service}-mcp.json`:
```json
{
  "{service}": {
    "command": "node",
    "args": ["/path/to/mcp/server/build/bin.js"],
    "env": {
      "CLIENT_ID": "${CLIENT_ID}",
      "CLIENT_SECRET": "${CLIENT_SECRET}"
    }
  }
}
```

### MCP server path pitfall (Python interpreter mismatch)

Hermes runs in a venv whose `python3` is Python 3.11. MCP servers that install under the system Python 3.13 (like mempalace) MUST use an absolute path in `~/.hermes/config.yaml`:

```yaml
mcp:
  mempalace:
    command: /usr/bin/python3   # NOT "python3"
    args:
      - -m
      - mempalace.mcp_server
    enabled: true
```

If bare `python3` is used, the MCP server silently fails at import (`ModuleNotFoundError`), and any skill depending on it will appear to "work" but produce no persisted data.

### MCP verification

- `hermes mcp test {server}` — confirm server responds
- Check MCP config at `~/.hermes/mcp/`, verify server path
- Test with `hermes mcp call` once registered
