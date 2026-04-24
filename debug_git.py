import subprocess, sys

def run(cmd, env=None):
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    print(f"Running: {cmd}")
    print(f"  returncode: {result.returncode}")
    print(f"  stdout: {result.stdout[:100] if result.stdout else 'empty'}")
    print(f"  stderr: {result.stderr[:200] if result.stderr else 'empty'}")
    if result.returncode != 0:
        raise RuntimeError(f"Failed: {result.stderr}")
    return result.stdout.strip()

try:
    commits = run(['git', 'rev-list', '--all', '--topo-order', '--reverse']).split('\n')
    commits = [c for c in commits if c]
    print(f"Found {len(commits)} commits")
    
    if commits:
        first = commits[0]
        print(f"First commit: {first}")
        obj = run(['git', 'cat-file', '-p', first])
        print(f"First 300 chars of cat-file:")
        print(obj[:300])
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
