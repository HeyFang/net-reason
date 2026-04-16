# net-reason

> AIKR (AI Knowledge Reasoning) — Network & Linux error diagnosis CLI

**net-reason** is a command-line tool that helps diagnose common Linux and Ubuntu network errors through a guided Y/N question flow. It maps your error to a known category, walks a decision tree to narrow down the root cause, and surfaces specific fix commands.

---

## Install

```bash
git clone https://github.com/you/net-reason
cd net-reason
pip install -e .
```

Or without cloning:

```bash
pip install -e /path/to/net-reason
```

---

## Usage

### Diagnose an error

```bash
# Interactive — paste or type your error
netreason diagnose

# Pass the error directly
netreason diagnose "temporary failure in name resolution"
netreason diagnose "could not get lock /var/lib/dpkg/lock"
netreason diagnose ssh
netreason diagnose dns
```

### List supported categories

```bash
netreason list
```

---

## How it works

1. You paste an error message or type a keyword
2. net-reason matches it to a category via keyword scoring
3. It asks a short series of Y/N questions to narrow down the condition
4. It outputs a root cause diagnosis + specific fix commands

The entire knowledge base lives in `data/errors.json` — it's a tree of questions and leaf-node diagnoses. Easy to extend.

---

## Supported error categories

| Category | Examples |
|---|---|
| **DNS Resolution** | `could not resolve host`, `temporary failure in name resolution` |
| **SSH Connection** | `connection refused`, `host key verification failed`, `permission denied (publickey)` |
| **APT Package Manager** | `could not get lock`, `unable to fetch`, `dpkg was interrupted` |
| **Network Connectivity** | `network unreachable`, `no route to host`, `interface down` |
| **Systemd / Services** | `failed to start`, `unit not found`, `masked`, `active: failed` |
| **Firewall / UFW** | `ufw`, `port blocked`, `iptables` |

---

## Extending the knowledge base

Edit `data/errors.json`. Each category follows this schema:

```json
{
  "id": "my_category",
  "name": "Human Name",
  "keywords": ["error keyword", "another phrase"],
  "description": "Short description",
  "tree": {
    "question": "Is X happening?",
    "yes": {
      "question": "Is Y also true?",
      "yes": {
        "diagnosis": "Root cause label",
        "cause": "Explanation of why this happens.",
        "fixes": [
          "First fix command or instruction",
          "Second option"
        ],
        "docs": "https://link-to-docs"
      },
      "no": { ... }
    },
    "no": { ... }
  }
}
```

Leaf nodes have `diagnosis`, `cause`, `fixes`, and `docs`.  
Branch nodes have `question`, `yes`, and `no`.

---

## Project structure

```
net-reason/
├── netreason/
│   ├── __init__.py
│   ├── cli.py        — CLI entry point and commands
│   ├── matcher.py    — Keyword-based category matching
│   ├── engine.py     — Decision tree walker
│   └── ui.py         — Terminal UI helpers
├── data/
│   └── errors.json   — Knowledge base
├── setup.py
└── README.md
```

---

## License

MIT
