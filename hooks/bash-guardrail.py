#!/usr/bin/env python3
"""
PreToolUse hook for Claude Code.
Blocks dangerous bash commands regardless of permission settings.
Exit 0 = allow, Exit 2 = block.
"""
import sys
import json
import re

# ─── Protected files ────────────────────────────────────────
# Any command referencing these paths is blocked.
# Catches shell commands, redirects, AND interpreter scripts
# (python3 -c, node -e, ruby -e, perl -e, etc.)
PROTECTED_FILES = [
    r"\.claude/settings\.json",
    r"\.claude/settings\.local\.json",
    r"\.claude/hooks/bash-guardrail\.py",
    r"\.zshrc",
    r"\.zprofile",
    r"\.bash_profile",
    r"\.bashrc",
    r"\.env",
    r"\.key",
    r"\.pem",
]
# ────────────────────────────────────────────────────────────

# ─── Deny list ──────────────────────────────────────────────
# Format: ("keyword/command", "regex pattern")
DENY = {
    # Destructive file operations
    "rm -rf":           r"\brm\s+-[a-z]*r[a-z]*f\b",
    "rm -fr":           r"\brm\s+-[a-z]*f[a-z]*r\b",
    "rm -r":            r"\brm\s+(-r\b|--recursive\b)",
    "mkfs":             r"\bmkfs\b",
    "dd":               r"\bdd\s+.*of=",
    "truncate":         r"\btruncate\b",
    "chmod 777":        r"\bchmod\s+777\b",
    "chown":            r"\bchown\b",

    # Git
    "git push --force": r"\bgit\s+push\b.*?(--force\b|-f\b)",
    "git push":         r"\bgit\s+push\b",

    # Infra / K8s
    "kubectl delete":   r"\bkubectl\s+delete\b",
    "kubectl drain":    r"\bkubectl\s+drain\b",
    "kubectl scale 0":  r"\bkubectl\s+scale\b.*--replicas[= ]*0\b",
    "helm uninstall":   r"\bhelm\s+(uninstall|delete)\b",
    "docker sys prune": r"\bdocker\s+system\s+prune\b",
    "brew uninstall":   r"\bbrew\s+uninstall\b",

    # Remote code execution
    "curl|wget pipe":   r"\b(curl|wget)\b.*\|\s*(ba)?sh\b",
    "sh < redirect":    r"^\s*(ba)?sh\s+<",

    # Publish (irreversible release)
    "npm publish":      r"\bnpm\s+publish\b",
    "gradle publish":   r"\bgradle\w*\s+publish\b",

    # Env/secret leak
    "printenv":         r"\bprintenv\b",
    "env dump":         r"^\s*env\s*$",
    "echo secret var":  r"\becho\b.*\$\{?\w*(TOKEN|SECRET|PASSWORD|KEY|CREDENTIAL)\w*\b",
    "show-token":       r"\bgh\s+auth\s+.*--show-token\b",

    # GitHub CLI
    "gh pr comment":    r"\bgh\s+pr\s+comment\b",
}
# ────────────────────────────────────────────────────────────

try:
    data = json.load(sys.stdin)
    cmd = data.get("tool_input", {}).get("command", "")
except Exception:
    sys.exit(0)

if not cmd:
    sys.exit(0)

# Check protected files — blocks ANY reference in the command
for pattern in PROTECTED_FILES:
    if re.search(pattern, cmd, re.IGNORECASE):
        print(f"BLOCKED: access to protected file ({pattern})", file=sys.stderr)
        sys.exit(2)

# Check deny list
for name, pattern in DENY.items():
    if re.search(pattern, cmd, re.IGNORECASE | re.MULTILINE):
        print(f"BLOCKED: {name} is not allowed", file=sys.stderr)
        sys.exit(2)

sys.exit(0)
