---
name: launchdarkly
description: Read or change Redo LaunchDarkly flags through the authenticated REST API, including team targeting, evaluation, rollout and rollback. Use the existing AWS SSM credential before a browser.
---

# LaunchDarkly

Use the API for flag inspection and authorized changes. The official `ldcli`
is optional; AWS CLI and Python's standard library are sufficient. Use the
browser only for an operation the API cannot perform or an authentication
step the user must complete.

## Credentials and Redo conventions

- API origin: `https://app.launchdarkly.com/api/v2`.
- Redo project: `default`. Production environment: `production`.
- API credential: `LAUNCH_DARKLY_TOKEN`. It is an access token, not the
  environment-specific `LAUNCH_DARKLY_SDK_KEY`.
- The canonical secret is AWS SSM SecureString
  `/RedoProduction/LaunchDarkly/Token` in `us-east-1`, production account
  `260890374087`. Verify the current mapping in the product checkout's
  `tools/local/secrets.args`.
- On Brendan's Mac, AWS profile `default` uses the existing production
  Developer identity. The app's `conf.sh` may select `dev`, which assumes a
  role in a different account. `ParameterNotFound` there does not establish
  that the LaunchDarkly credential is missing.
- Verify identity with `aws sts get-caller-identity --profile default`.
  Use the intended configured profile, not a succession of broader roles.
  Expired authentication requires the normal AWS SSO login. An access denial
  is an access limit, not a reason to change roles or create a new token.

Never print the token, put it in shell arguments, copy it into artifacts, or
save it in this repository. The helper below uses an existing exported token
first, otherwise captures the one SSM value in memory. It sends the token in
the `Authorization` header without a `Bearer` prefix and pins API version
`20240415`. It does not source the app's shell configuration or load all secrets.

## Read and evaluate

Resolve the helper relative to this skill's directory:

```bash
python3 scripts/launchdarkly.py get --flag FLAG_KEY --env production
```

The response includes variation values and IDs, global `_version`, and the
requested environment's `on`, `version`, `offVariation`, `fallthrough`,
`contextTargets`, `targets`, `rules` and prerequisites. Determine true and
false variation IDs from their values; do not assume index zero is false.
Read the application flag definition to establish its context kind and
targeting key. Redo's `teamContext` uses kind `team` and the Mongo team ID,
not a warehouse account ID or the legacy default `user` kind.

To evaluate a context, write its JSON to a local task file and run:

```bash
python3 scripts/launchdarkly.py evaluate --flag FLAG_KEY --env production \
  --body /absolute/path/to/context.json
```

For example, a team context is `{"kind":"team","key":"TEAM_ID"}`. Include
the same attributes as the application when rules depend on them. Evaluation
is read-only. Inspect the matching item's `_value` and evaluation reason.
Check an intended target and an unrelated control context.

## Make the authorized change

Loading this skill does not authorize changing production. Carry forward the
user's actual rollout approval and its cohort, observation window and rollback
plan. A deployed MR does not itself authorize flag activation.

1. Read and retain the current flag configuration in the task output directory.
   Check the requested environment, variation values, prerequisites, rules,
   targets and fallthrough. Confirm the production deployment contains the code.
2. Prepare the smallest patch for the approved effect. Preserve other teams'
   targeting. Prefer semantic instructions such as `addTargets` and
   `removeTargets` with explicit `contextKind: "team"`, and the variation's
   actual `_id`. A semantic body includes `environmentKey`, `instructions`
   and a comment naming the ticket and reason.
   For a percentage rollout of a team flag, specify `rolloutContextKind:
   "team"` and stable key bucketing. Verify the API's weight units rather than
   treating percentage weights as whole percents.
3. For an initially disabled canary, inspect the enabled fallthrough before
   turning targeting on. If it is true, configure false as the fallback before
   or atomically with adding the canary target and turning targeting on.
   Otherwise enabling the flag can expose every unlisted team.
4. Re-read immediately before applying. If the reviewed version or owned fields
   changed, reconcile the new state instead of overwriting it. Use a JSON Patch
   `test` operation when an atomic field precondition is needed. Do not blindly
   retry an ambiguous write; read back first.
5. Apply the prepared body only within the authorized scope:

```bash
python3 scripts/launchdarkly.py patch --flag FLAG_KEY --env production \
  --body /absolute/path/to/patch.json --semantic --apply
```

Without `--semantic`, the helper sends standard JSON content. Use the current
API documentation for the JSON Patch envelope. The helper's `--apply` is an
execution guard, not release approval.

Read the flag again and evaluate both target and control contexts. Save the
request, response, versions, timestamp and verification in the task record,
without credentials. Verify actual application requests and telemetry before
claiming exposure or a successful rollout. Do not shorten the agreed watch
window or remove the losing path before its rollout criteria pass.

Rollback should restore only this task's owned targeting. Turning targeting
off is appropriate when the task owns the entire flag and its off variation
is verified safe. Do not replace shared rules or targets from an old snapshot.
Archive a flag only after deployed code no longer depends on it and the task's
cleanup authorization covers that action.

## Source and failures

The product client lives at `redo/feature-flags/client/src/client.ts`; typed
context definitions are in `redo/feature-flags/model`, and conventions are in
`docs/feature-flag.md`. Reuse existing client operations in application code.
Do not run Bazel or manage scripts locally to obtain a token. The helper is
standalone operational tooling, not an application build.

- Authentication or permission errors: report the exact AWS or HTTP failure
  without its secret. Do not infer write permission from a successful read.
- HTTP 409 or a failed patch precondition: re-read and reconcile.
- HTTP 429: respect `Retry-After`. Inspect state before retrying a write.
- Some endpoints, such as evaluation usage, require `LD-API-Version: beta`.
  A 403 explicitly requesting that header is a version requirement, not proof
  the token lacks permission. Use beta only for that documented operation.
  For `GET /usage/evaluations/{project}/{environment}/{flag}`, pass `from` and
  `to` as Unix epoch milliseconds. Verify the returned bucket timestamps. In
  the verified API, ISO strings silently returned the default 30-day range.
  The response's `metadata` maps numbered series to variation values; these
  counts do not identify individual contexts or prove application correctness.
- A missing MCP tool or an empty exported environment does not mean API
  access is unavailable. Check the documented SSM route first.

Official references, verify the specific operation before using unfamiliar fields:

- [Authentication and API versioning](https://launchdarkly.com/docs/api/overview)
- [Get feature flag](https://launchdarkly.com/docs/api/feature-flags/get-feature-flag)
- [Update feature flag and semantic instructions](https://launchdarkly.com/docs/api/feature-flags/update-feature-flag)
- [Evaluation usage](https://launchdarkly.com/docs/api/account-usage-beta/get-evaluations-usage)
