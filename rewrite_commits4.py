import subprocess
import re
import os
import traceback
import sys

KARPATHY_EMAILS = {'andrej.karpathy@gmail.com', 'akarpathy@tesla.com'}
NEW_NAME = 'Logiclayer1111'
NEW_EMAIL = 'atn2122804@gmail.com'

log = open('rewrite_debug4.txt', 'w', encoding='utf-8', buffering=1)

def run(cmd, env=None, input_text=None):
    log.write(f"Running: {cmd}\n")
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True, 
        encoding='utf-8', 
        errors='replace',
        env=env, 
        input=input_text
    )
    log.write(f"  returncode: {result.returncode}\n")
    if result.stderr:
        log.write(f"  stderr: {result.stderr[:300]}\n")
    if result.returncode != 0:
        raise RuntimeError(f"Failed: {result.stderr}")
    return result.stdout.strip()

try:
    commits = run(['git', 'rev-list', '--all', '--topo-order', '--reverse']).split('\n')
    commits = [c for c in commits if c]
    log.write(f"Found {len(commits)} commits\n")

    old_to_new = {}

    for idx, old_commit in enumerate(commits):
        log.write(f"[{idx+1}/{len(commits)}] Processing {old_commit[:8]}\n")
        
        obj = run(['git', 'cat-file', '-p', old_commit])
        lines = obj.split('\n')
        
        tree = None
        parents = []
        author_line = None
        committer_line = None
        message_start = 0
        
        for i, line in enumerate(lines):
            if line.startswith('tree '):
                tree = line[5:]
            elif line.startswith('parent '):
                parents.append(line[7:])
            elif line.startswith('author '):
                author_line = line[7:]
                message_start = i + 1
            elif line.startswith('committer '):
                committer_line = line[10:]
                message_start = i + 1
            elif line == '':
                message_start = i + 1
                break
        
        message = '\n'.join(lines[message_start:])
        
        author_match = re.match(r'(.+) <([^>]+)> (\d+ [+-]\d+)', author_line)
        committer_match = re.match(r'(.+) <([^>]+)> (\d+ [+-]\d+)', committer_line)
        
        if not author_match or not committer_match:
            log.write(f"  Failed to parse author/committer, skipping\n")
            continue
        
        old_author_name = author_match.group(1)
        old_author_email = author_match.group(2)
        author_date = author_match.group(3)
        
        old_committer_name = committer_match.group(1)
        old_committer_email = committer_match.group(2)
        committer_date = committer_match.group(3)
        
        log.write(f"  Author: {old_author_name} <{old_author_email}>\n")
        
        if old_author_email in KARPATHY_EMAILS:
            new_author_name = NEW_NAME
            new_author_email = NEW_EMAIL
            new_committer_name = NEW_NAME
            new_committer_email = NEW_EMAIL
            log.write(f"  -> Will rewrite to {NEW_NAME}\n")
        else:
            new_author_name = old_author_name
            new_author_email = old_author_email
            new_committer_name = old_committer_name
            new_committer_email = old_committer_email
        
        cmd = ['git', 'commit-tree', tree]
        for p in parents:
            mapped_parent = old_to_new.get(p, p)
            cmd.extend(['-p', mapped_parent])
        
        env = os.environ.copy()
        env['GIT_AUTHOR_NAME'] = new_author_name
        env['GIT_AUTHOR_EMAIL'] = new_author_email
        env['GIT_AUTHOR_DATE'] = author_date
        env['GIT_COMMITTER_NAME'] = new_committer_name
        env['GIT_COMMITTER_EMAIL'] = new_committer_email
        env['GIT_COMMITTER_DATE'] = committer_date
        
        new_commit = run(cmd, env=env, input_text=message)
        old_to_new[old_commit] = new_commit
        
        log.write(f"  Rewrote -> {new_commit[:8]}\n")

    log.write("Updating refs...\n")
    refs = run(['git', 'for-each-ref', '--format=%(refname)']).split('\n')
    for ref in refs:
        if not ref or ref.startswith('refs/remotes/') or ref.startswith('refs/original/'):
            continue
        try:
            old_hash = run(['git', 'rev-parse', ref])
            new_hash = old_to_new.get(old_hash, old_hash)
            run(['git', 'update-ref', ref, new_hash])
            log.write(f"Updated {ref} -> {new_hash[:8]}\n")
        except Exception as e:
            log.write(f"Skipped {ref}: {e}\n")

    log.write("Done!\n")
    log.close()
    print("Done! Check rewrite_debug4.txt for details.")
    
except Exception as e:
    log.write(f"ERROR: {e}\n")
    log.write(traceback.format_exc())
    log.close()
    print(f"ERROR: {e}")
    sys.exit(1)
