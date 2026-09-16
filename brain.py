#!/usr/bin/env python3
"""
Kitten Pomodoro Brain — logs cycles and decides long breaks.
150-min window: 4 consecutive work pomodoros within 150 min → next break 20 min.
"""
import json, time
from pathlib import Path
from datetime import datetime, timedelta

LOG = Path(__file__).parent / "pomodoro.jsonl"
LOG.parent.mkdir(parents=True, exist_ok=True)

def _now_iso():
    return datetime.now().isoformat(timespec="seconds")

def log_event(etype, duration_min, completed=True, extra=None):
    """etype: work|break|reset"""
    entry = {"ts": _now_iso(), "type": etype, "duration": duration_min, "completed": completed}
    if extra: entry.update(extra)
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

def log_work_completed(duration=25):
    return log_event("work", duration, True)

def log_break_completed(duration):
    return log_event("break", duration, True)

def log_reset():
    return log_event("reset", 0, False)

def _load_events():
    if not LOG.exists():
        return []
    events=[]
    for line in LOG.read_text().splitlines():
        line=line.strip()
        if not line: continue
        try:
            events.append(json.loads(line))
        except: continue
    return events

def consecutive_work_count(within_min=150):
    """Count consecutive completed work pomodoros at the tail, within window, no reset/long-break in between."""
    events = _load_events()
    consecutive=[]
    cutoff = datetime.now() - timedelta(minutes=within_min)
    for e in reversed(events):
        try:
            ts = datetime.fromisoformat(e["ts"])
        except:
            continue
        if ts < cutoff:
            break
        if e["type"] == "reset":
            break
        if e["type"] == "break" and e.get("duration") == 20 and e["completed"]:
            break
        if e["type"] == "work" and e["completed"]:
            consecutive.append(e)
            if len(consecutive) >= 4:
                break
        elif e["type"] == "work" and not e["completed"]:
            break
    return len(consecutive)

def next_break_minutes(within_min=150):
    """Call right after a work pomodoro completes, before starting break.
       Returns 20 if 4th in row within window, else 5."""
    cnt = consecutive_work_count(within_min)
    if cnt >= 4 and cnt % 4 == 0:
        return 20
    return 5

def stats():
    events=_load_events()
    works=len([e for e in events if e["type"]=="work" and e["completed"]])
    breaks=len([e for e in events if e["type"]=="break" and e["completed"]])
    consec=consecutive_work_count()
    return {"works": works, "breaks": breaks, "consecutive": consec, "next_break": next_break_minutes()}

if __name__ == "__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="--stats":
        print(json.dumps(stats(), indent=2))
    elif len(sys.argv)>1 and sys.argv[1]=="--log":
        log_work_completed()
        print("logged work, next break", next_break_minutes())
    else:
        print(stats())
