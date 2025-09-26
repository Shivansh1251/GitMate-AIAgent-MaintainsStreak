#!/usr/bin/env python3
"""
GitMate daily uploader (takes paths from config, copies into repo, commits & pushes).
"""

import os
import sys
import yaml
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import argparse
import random

SCRIPT_DIR = Path(__file__).resolve().parent

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_state(path):
    if not path.exists():
        state = {"last_index": -1, "day_count": 0}
        save_state(path, state)
        return state
    with open(path, "r") as f:
        return json.load(f)

def save_state(path, state):
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def run(cmd, cwd=None, env=None, check=True):
    print(">", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, env=env, check=check, text=True, capture_output=False)

def run_output(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd).decode().strip()

def ensure_repo(repo_local, repo_remote):
    git_dir = repo_local / ".git"
    if git_dir.exists():
        print("Repo already cloned at", repo_local)
        return
    # Clone
    print("Cloning remote repo...")
    run(["git", "clone", repo_remote, str(repo_local)])

def gather_sources(cfg):
    # Expand and normalize paths
    if cfg.get("source_paths"):
        sources = [Path(os.path.expanduser(p)) for p in cfg["source_paths"]]
    elif cfg.get("source_dir"):
        d = Path(os.path.expanduser(cfg["source_dir"]))
        sources = sorted([p for p in d.iterdir() if p.name != ".git"])
    else:
        raise ValueError("No source_paths or source_dir in config.")
    # keep only existing
    sources = [p for p in sources if p.exists()]
    if not sources:
        raise ValueError("No existing source files found.")
    return sources

def pick_source(sources, strategy, state):
    if strategy == "single":
        return sources[0], 0
    if strategy == "random":
        idx = random.randrange(len(sources))
        return sources[idx], idx
    # rotate by index
    last = state.get("last_index", -1)
    idx = (last + 1) % len(sources)
    return sources[idx], idx

def safe_copy(src: Path, dst: Path):
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

def git_has_changes(repo_local):
    out = run_output(["git", "status", "--porcelain"], cwd=repo_local)
    return bool(out.strip())

def git_add_commit_push(repo_local, commit_message, branch, ssh_key_path=None):
    run(["git", "add", "--all"], cwd=repo_local)
    if not git_has_changes(repo_local):
        print("No changes to commit.")
        return False
    run(["git", "commit", "-m", commit_message], cwd=repo_local)
    env = os.environ.copy()
    if ssh_key_path:
        # Force git to use the provided key (safe for cron)
        env["GIT_SSH_COMMAND"] = f"ssh -i {ssh_key_path} -o IdentitiesOnly=yes -o StrictHostKeyChecking=no"
    run(["git", "push", "origin", branch], cwd=repo_local, env=env)
    return True

def main(config_path, dry_run=False):
    cfg = load_yaml(config_path)
    repo_local = Path(os.path.expanduser(cfg["repo_local_path"]))
    repo_remote = cfg["repo_remote"]
    branch = cfg.get("branch", "main")
    dest_sub = cfg.get("dest_subfolder", "uploads")
    strategy = cfg.get("upload_strategy", "rotate")
    ssh_key = cfg.get("ssh_key_path") if cfg.get("auth_method") == "ssh" else None

    state_path = SCRIPT_DIR / "state.json"
    state = load_state(state_path)

    ensure_repo(repo_local, repo_remote)

    sources = gather_sources(cfg)
    src_path, chosen_idx = pick_source(sources, strategy, state)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    base = src_path.name
    dest_name = f"{today}_{base}"
    dest_path = repo_local / dest_sub / dest_name

    print(f"Selected source: {src_path}")
    print(f"Destination (in repo): {dest_path}")

    if dry_run:
        print("[dry-run] Would copy now, then git add/commit/push.")
        return

    # copy
    if dest_path.exists():
        # avoid overwrite: append timestamp
        t = datetime.utcnow().strftime("%H%M%S")
        dest_name = f"{today}_{t}_{base}"
        dest_path = repo_local / dest_sub / dest_name

    print("Copying...")
    safe_copy(src_path, dest_path)

    # commit & push
    day_count = state.get("day_count", 0) + 1
    msg_tpl = cfg.get("commit_message_template", "Day {day}: {name}")
    commit_message = msg_tpl.format(day=day_count, name=base)

    try:
        pushed = git_add_commit_push(repo_local, commit_message, branch, ssh_key_path=ssh_key)
    except subprocess.CalledProcessError as e:
        print("Git operation failed:", e)
        raise

    if pushed:
        # update state
        state["last_index"] = chosen_idx
        state["day_count"] = day_count
        save_state(state_path, state)
        print("Upload complete and pushed.")
    else:
        print("Nothing to push; state not updated.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", "-c", default=str(SCRIPT_DIR / "config.yaml"))
    ap.add_argument("--dry-run", action="store_true", help="Do everything except commit/push")
    args = ap.parse_args()
    main(args.config, dry_run=args.dry_run)
