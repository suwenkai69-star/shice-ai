from __future__ import annotations

import argparse
import time
from pathlib import Path

from notifications.wechat import WechatSubscriptionProvider
from services.reminder_service import ReminderService


def main() -> int:
    parser = argparse.ArgumentParser(description="Dispatch due 食策AI Mini reminders")
    parser.add_argument("--db", default="data/shice_ai.db")
    parser.add_argument("--now", type=int, default=None, help="epoch milliseconds; defaults to current time")
    args = parser.parse_args()
    now = args.now if args.now is not None else int(time.time() * 1000)
    results = ReminderService(Path(args.db), WechatSubscriptionProvider()).dispatch_due(now)
    counts = {"SENT": 0, "FAILED": 0, "SKIPPED": 0}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    print(f"SENT={counts['SENT']} FAILED={counts['FAILED']} SKIPPED={counts['SKIPPED']}")
    return 1 if counts["FAILED"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
