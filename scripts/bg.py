#!/usr/bin/env python3
# ci-line: Background launcher (bg.py starts a command detached and records its PID in <worktree>/.claude/pids.json; the registry reads back and is gitignored) | --selftest
# ci-deps: scripts/end-task.py .gitignore
"""Start a long-running command in the background and RECORD it, so end-task.py can stop it (contract BG-LAUNCHER).

Servers and wait loops that a session starts in the background outlive the session, and a leftover server makes a
worktree removal fail with "Permission denied". Hunting processes by command line is guesswork, so the fix is at
launch: register the process here, and `scripts/end-task.py` stops what was registered before it removes the worktree.

    python scripts/bg.py -- python scripts/serve-stubbed.py 8801        # prints the PID
    python scripts/bg.py --worktree E:/jon/mg-x -- python -m http.server 8802
    python scripts/bg.py --list                                         # what this worktree has registered
    python scripts/bg.py --selftest

The registry is <worktree>/.claude/pids.json (gitignored): a list of {pid, create, cmd, started, worktree}. `create`
is the process's own creation time, read back from the OS, so a recycled PID is never mistaken for the original.
The command's output goes to <worktree>/.claude/bg-<pid>.log (gitignored). The worktree is the git top level of the
current directory unless --worktree says otherwise. Works on Windows (a detached process, stopped with taskkill /T)
and POSIX (its own session and process group, stopped as a group).

NOT covered: harness-managed background shells (the Bash tool's run_in_background); stop those with the harness.
"""
import json
import os
import subprocess
import sys
import tempfile
import time

WIN = os.name == "nt"


def toplevel(cwd=None):
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    return os.path.normpath(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None


def registry_path(worktree):
    return os.path.join(worktree, ".claude", "pids.json")


def read_registry(worktree):
    try:
        with open(registry_path(worktree), encoding="utf-8", newline="") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def write_registry(worktree, entries):
    p = registry_path(worktree)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        json.dump(entries, fh, indent=1)
        fh.write("\n")


def create_time(pid):
    """The OS's creation time for a live pid as a string (None if it is gone): identifies the process, not the number."""
    if WIN:
        ps = "$p=Get-CimInstance Win32_Process -Filter 'ProcessId=%d'; if($p){$p.CreationDate.ToUniversalTime().ToString('o')}" % pid
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True, text=True,
                           encoding="utf-8")
    else:
        try:
            r = subprocess.run(["ps", "-p", str(pid), "-o", "stat=,lstart="], capture_output=True, text=True, encoding="utf-8")
            out = r.stdout.strip()
            return None if not out or out.startswith("Z") else out.split(None, 1)[-1]   # a zombie is already dead
        except FileNotFoundError:                       # a container without procps: /proc/<pid>/stat, state then start ticks
            try:
                with open("/proc/%d/stat" % pid) as fh:
                    f = fh.read().rsplit(")", 1)[1].split()
                return None if f[0] == "Z" else f[19]
            except (OSError, IndexError):
                return None
    return r.stdout.strip() or None


def start(cmd, worktree):
    """Start cmd detached, register it under worktree, return the entry."""
    os.makedirs(os.path.join(worktree, ".claude"), exist_ok=True)
    log = open(os.path.join(worktree, ".claude", "bg-%d.log" % int(time.time() * 1000)), "wb")
    kw = {"stdin": subprocess.DEVNULL, "stdout": log, "stderr": subprocess.STDOUT, "cwd": worktree}
    if WIN:
        kw["creationflags"] = 0x00000008 | 0x00000200      # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    else:
        kw["start_new_session"] = True
    p = subprocess.Popen(cmd, **kw)
    log.close()
    entry = {"pid": p.pid, "create": None, "cmd": cmd, "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "worktree": worktree}
    for _ in range(20):                                      # the OS needs a moment to show the new process
        entry["create"] = create_time(p.pid)
        if entry["create"]:
            break
        time.sleep(0.1)
    entries = read_registry(worktree)
    entries.append(entry)
    write_registry(worktree, entries)
    return entry


def selftest():
    import importlib.util
    spec = importlib.util.spec_from_file_location("end_task", os.path.join(os.path.dirname(os.path.abspath(__file__)), "end-task.py"))
    et = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(et)
    fails = []

    def check(name, ok):
        print("  %s  %s" % ("PASS" if ok else "FAIL", name))
        if not ok:
            fails.append(name)

    sleeper = "import time; time.sleep(300)"
    with tempfile.TemporaryDirectory() as td:
        wt = os.path.join(td, "wt")
        os.makedirs(wt)
        childfile = os.path.join(wt, "child.pid")
        parent_code = ("import subprocess, sys, time\n"
                       "c = subprocess.Popen([sys.executable, '-c', %r])\n"
                       "open(%r, 'w').write(str(c.pid))\n"
                       "time.sleep(300)\n" % (sleeper, childfile))
        planted = None
        try:
            e = start([sys.executable, "-c", parent_code], wt)
            for _ in range(60):
                if os.path.exists(childfile) and open(childfile).read().strip():
                    break
                time.sleep(0.1)
            child = int(open(childfile).read().strip())
            check("bg.py registered the sleeper (pid, command, start time, worktree)",
                  e["pid"] > 0 and e["create"] and e["worktree"] == wt and read_registry(wt)[0]["pid"] == e["pid"])
            check("the sleeper and its child are alive", et.alive(e["pid"], e["create"]) and et.alive(child))
            # an unregistered process whose command line holds the worktree path
            planted = subprocess.Popen([sys.executable, "-c", sleeper, os.path.join(wt, "planted")])
            time.sleep(0.5)
            stopped = et.stop_registered(wt)
            time.sleep(0.5)
            check("the registered process is stopped", not et.alive(e["pid"], e["create"]) and stopped and stopped[0][0] == e["pid"])
            check("its child is stopped too", not et.alive(child))
            check("the registry is cleared", read_registry(wt) == [] and not os.path.exists(registry_path(wt)))
            seen = [p for p, _ in et.unregistered(wt, exclude={os.getpid()})]
            check("the planted unregistered process is reported", planted.pid in seen)
            check("the planted process was reported, not killed", planted.poll() is None)
        finally:
            if planted is not None:
                planted.kill()
                planted.wait()
            try:
                et.stop_registered(wt)
            except Exception:
                pass
            for pid in (locals().get("child"),):
                if pid:
                    et.kill_tree(pid)
    print("selftest: %s" % ("FAILED: " + ", ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    wt = None
    if argv[:1] == ["--list"]:
        wt = toplevel() or os.getcwd()
        for e in read_registry(wt):
            print("%s  %s  %s" % (e["pid"], e["started"], " ".join(e["cmd"])))
        return 0
    if argv[:1] == ["--worktree"] and len(argv) > 2:
        wt, argv = os.path.normpath(argv[1]), argv[2:]
    if not argv or argv[0] != "--" or len(argv) < 2:
        print(__doc__)
        return 2
    wt = wt or toplevel() or os.getcwd()
    e = start(argv[1:], wt)
    print(e["pid"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
