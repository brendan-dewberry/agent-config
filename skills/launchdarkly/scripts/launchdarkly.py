#!/usr/bin/env python3
"""Use Redo's existing access token for a bounded LaunchDarkly flag request."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("LaunchDarkly redirected the request; no credential was forwarded.")


def load_token(profile):
    token = os.environ.get("LAUNCH_DARKLY_TOKEN")
    if token:
        return token
    result = subprocess.run(
        [
            "aws", "ssm", "get-parameter", "--profile", profile,
            "--region", "us-east-1", "--name", "/RedoProduction/LaunchDarkly/Token",
            "--with-decryption", "--output", "json", "--no-cli-pager",
        ],
        capture_output=True, text=True, timeout=45,
    )
    if result.returncode:
        raise RuntimeError("AWS SSM credential lookup failed: " + result.stderr.strip())
    token = json.loads(result.stdout)["Parameter"]["Value"]
    if not isinstance(token, str) or not token:
        raise RuntimeError("AWS SSM returned an empty LaunchDarkly token.")
    return token


def read_body(path):
    if not path:
        raise ValueError("--body is required for evaluate and patch.")
    return json.loads(Path(path).read_text())


def request_flag(args):
    project, flag, env = [
        urllib.parse.quote(value, safe="")
        for value in (args.project, args.flag, args.env)
    ]
    body = None
    method = "GET"
    content_type = "application/json"
    path = f"/flags/{project}/{flag}?env={env}"
    if args.operation == "evaluate":
        body = read_body(args.body)
        method = "POST"
        query = urllib.parse.urlencode({"filter": f"query equals {args.flag}"})
        path = f"/projects/{project}/environments/{env}/flags/evaluate?{query}"
    elif args.operation == "patch":
        if not args.apply:
            raise ValueError("Patch requires --apply and existing authorization for its effects.")
        body = read_body(args.body)
        method = "PATCH"
        path = f"/flags/{project}/{flag}"
        if args.semantic:
            if not isinstance(body, dict) or body.get("environmentKey") != args.env:
                raise ValueError("Semantic patch environmentKey must match --env.")
            content_type += "; domain-model=launchdarkly.semanticpatch"
    elif args.body or args.semantic or args.apply:
        raise ValueError("get does not accept --body, --semantic or --apply.")
    token = load_token(args.profile)
    request = urllib.request.Request(
        "https://app.launchdarkly.com/api/v2" + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": token,
            "LD-API-Version": "20240415",
            "Content-Type": content_type,
        },
        method=method,
    )
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        message = error.read().decode(errors="replace")[:1000].replace(token, "<redacted>")
        retry_after = error.headers.get("Retry-After")
        retry_note = f" Retry-After: {retry_after}." if retry_after else ""
        raise RuntimeError(f"LaunchDarkly HTTP {error.code}: {message}.{retry_note}") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["get", "evaluate", "patch"])
    parser.add_argument("--flag", required=True)
    parser.add_argument("--project", default="default")
    parser.add_argument("--env", default="production")
    parser.add_argument("--profile", default="default")
    parser.add_argument("--body", help="JSON request file, never a credential file")
    parser.add_argument("--semantic", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(request_flag(args), indent=2))
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
