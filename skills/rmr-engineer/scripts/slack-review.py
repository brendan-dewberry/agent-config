#!/usr/bin/env python3
"""Check Patch's identity or send the RMR workflow's two-line review request."""

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


PATCH_USER_ID = "U0CF7BZGGAZ"
WORKSPACE_ID = "T012MLH7MRT"
REVIEW_CHANNEL_ID = "C0938J181B8"


class SlackError(Exception):
    pass


def call_slack(token, method, fields=None, *, get=False):
    url = "https://slack.com/api/" + method
    if get:
        url += "?" + urllib.parse.urlencode(fields or {})
    request = urllib.request.Request(
        url,
        data=None if get else json.dumps(fields or {}).encode(),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json; charset=utf-8",
        },
        method="GET" if get else "POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        raise SlackError(f"{method}: HTTP {error.code}") from None
    except (urllib.error.URLError, TimeoutError, ValueError):
        raise SlackError(f"{method}: transport or response failure") from None
    if not result.get("ok"):
        raise SlackError(f"{method}: {result.get('error', 'unknown_error')}")
    return result


def review_message(args):
    title = re.sub(r"^Draft:\s*", "", args.title).strip()
    if not title or any(char in title for char in "\r\n"):
        raise SlackError("The actual MR title must be one nonempty line")
    url = urllib.parse.urlsplit(args.mr_url)
    if (
        url.scheme != "https"
        or url.netloc != "lgtm.redo.builders"
        or any(char in args.mr_url for char in "\r\n<>|")
    ):
        raise SlackError("Use the verified LGTM review URL")
    if not re.fullmatch(r"U[A-Z0-9]+", args.reviewer):
        raise SlackError("Use the assigned review owner's verified Slack user ID")
    return (
        f"*{html.escape(title, quote=False)}*\n"
        f"<{args.mr_url}|Review MR !{args.mr_iid}> · <@{args.reviewer}>"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--token-file", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Check identity only")
    mode.add_argument("--post", action="store_true", help="Send a review request")
    parser.add_argument("--title")
    parser.add_argument("--mr-url")
    parser.add_argument("--mr-iid", type=int)
    parser.add_argument("--reviewer")
    parser.add_argument("--thread-ts", help="Existing review thread for an update")
    args = parser.parse_args()
    if args.post and (
        not all([args.title, args.mr_url, args.mr_iid, args.reviewer])
        or args.mr_iid < 1
    ):
        parser.error("--post requires --title, --mr-url, --mr-iid and --reviewer")
    message = review_message(args) if args.post else None
    try:
        token = args.token_file.expanduser().read_text().strip()
    except OSError:
        raise SlackError("Cannot read the configured token file") from None
    if not token:
        raise SlackError("The configured token file is empty")
    identity = call_slack(token, "auth.test")
    if (
        identity.get("user_id") != PATCH_USER_ID
        or identity.get("team_id") != WORKSPACE_ID
        or not identity.get("bot_id")
    ):
        raise SlackError("Credential does not authenticate as Patch in Redo")
    receipt = {"sender_user_id": PATCH_USER_ID, "sent": False}
    if args.check:
        print(json.dumps(receipt))
        return
    fields = {
        "channel": REVIEW_CHANNEL_ID,
        "text": message,
        "unfurl_links": False,
        "unfurl_media": False,
    }
    if args.thread_ts:
        fields["thread_ts"] = args.thread_ts
    try:
        sent = call_slack(token, "chat.postMessage", fields)
    except SlackError as error:
        raise SlackError(
            f"{error}. Inspect channel history before retrying; delivery may be uncertain"
        ) from None
    receipt.update(sent=True, channel_id=sent["channel"], message_ts=sent["ts"])
    try:
        link = call_slack(
            token,
            "chat.getPermalink",
            {"channel": sent["channel"], "message_ts": sent["ts"]},
            get=True,
        )
        receipt["permalink"] = link["permalink"]
    except SlackError as error:
        receipt["permalink_error"] = str(error)
    print(json.dumps(receipt))


if __name__ == "__main__":
    try:
        main()
    except SlackError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
