---
name: redo-agents-api
description: Use the authenticated Redo Agents HTTP API to inspect or manage agents, source, evals, checks, publications, and Works. Use for questions about agents.redo.builders, RMR Engineer, agent publication or evaluation status, or the stored Redo Agents API key.
---

# Redo Agents API

Use the Redo Agents HTTP API before the browser when working with agent source,
evals, checks, publication state, or Works. The absence of a dedicated MCP
connector does not mean API access is unavailable.

## Authenticate safely

The API origin is `https://agents.redo.builders` and is reachable over
Tailscale. Read the credential from `REDO_AGENTS_API_KEY`, falling back to
`~/.config/redo-agents/api-key`. Attach it as a Bearer token in the HTTP client.

- Never print, log, paste, or commit the key.
- Do not enable shell tracing or verbose HTTP output that could reveal the
  Authorization header.
- Start with `GET /v2/me`. Confirm the principal and scopes without echoing the
  credential. If the request fails, report the exact status and error safely.
- Check the returned scopes before selecting an endpoint. `author` access
  covers agent authoring and checks. Some private diagnostics require
  `operator` access. Do not treat a scope denial as proof the API is unavailable.

## Read the current API contract

Fetch `GET /v2/authoring/api` and the relevant route page under
`/v2/authoring/api/...` before relying on remembered endpoint details. Use
`GET /v2/openapi.json` when you need the exact schema. The API guide and route
documentation are the source of truth because endpoints and scope rules can
change.

## Investigate an agent or publication

For a read-only investigation:

1. Read `GET /v2/agent-projects/:slug` and inspect only the relevant files.
   Record its revision and tree identity.
2. Read `GET /v2/agent-projects/:slug/publications`. Open the relevant record
   with `GET /v2/publications/:id`; compare its `gitCommit`, state, stage,
   diagnostic, and evidence with the source revision.
3. Read `GET /v2/agent-projects/:slug/checks` and, when needed,
   `GET /v2/checks/:id`. Do not start a check or eval unless the user asked for
   it or the task clearly authorizes running it.
4. For an eval failure, compare its assertions with the agent instructions,
   eval fixture, selected skill, and published tool discovery. An available
   tool is not evidence that the agent called it. Treat an assertion failure
   as the observed cause; inspect the Work or private diagnostics for the
   exact turn-level trace when the key's scope permits it.
5. Report the exact commit, publication or check state, diagnostic, and any
   access limit. Keep configured, published, fixture-tested, and observed-live
   states distinct.

`GET /v2/publications/:id/diagnostics` may be restricted to operator keys.
If an author key receives `403 access_denied`, use the publication record and
other endpoints it can access, then state that the private trace needs an
operator key. Do not guess what the unavailable trace contains.

## Keep reads and writes separate

Use `GET` requests for status questions. A key may also have write permission,
but that does not authorize a save, validation run, eval, trigger change, or
publication action. Saves can publish agent source automatically. Before any
write, confirm that it is required by the user's request, check the current
revision, follow the route's idempotency and stale-revision rules, and report
the resulting publication state.

Use the browser only when the route documentation says the operation is
browser-only, when the user needs to interact with a browser flow, or when API
access is unavailable or insufficient. Explain the specific limitation before
switching to the browser.
