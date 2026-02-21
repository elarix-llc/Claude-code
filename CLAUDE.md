# CLAUDE.md

This file provides guidance to AI assistants (Claude Code and similar tools) working in this repository.

## Project Overview

**Repository:** `elarix-llc/Claude-code`
**License:** Apache 2.0
**Status:** Early-stage / bootstrapping

This is a new project. As of the initial commit the repository contains only the Apache 2.0 `LICENSE` file and a stub `README.md`. This document will be updated as the codebase grows.

## Repository Structure

```
Claude-code/
├── LICENSE          # Apache 2.0 license
├── README.md        # Project overview (stub — to be expanded)
└── CLAUDE.md        # This file
```

No source code, package manifests, or build configuration exist yet. When new directories and files are added, update this structure section accordingly.

## Git Workflow

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Stable, production-ready state |
| `claude/<topic>-<id>` | AI-driven feature/fix branches |

Branch names for AI-assisted work **must** follow the pattern `claude/<topic>-<id>` (e.g., `claude/add-claude-documentation-RCOdp`). Pushes to any other pattern from an AI session will be rejected.

### Commit conventions

- Write short, imperative subject lines (≤ 72 characters): `Add authentication module`, not `Added authentication module`.
- Add a blank line after the subject when a body is needed.
- Reference issue or PR numbers where relevant: `Fix null-pointer in parser (#42)`.
- Do not amend published commits; create a new commit instead.

### Push procedure

```bash
git push -u origin <branch-name>
```

On network failure, retry with exponential back-off: 2 s → 4 s → 8 s → 16 s (maximum 4 retries).

### Pull requests

- Title: concise, ≤ 70 characters.
- Body: bullet-point summary + test plan.
- Target branch: `main` (unless instructed otherwise).

## Development Conventions

These conventions apply from the first line of real code and should be followed consistently.

### General

- Prefer editing existing files over creating new ones.
- Delete unused code completely; do not comment it out or leave `_unused` aliases.
- Do not add error handling, fallbacks, or validation for scenarios that cannot occur.
- Do not introduce abstractions or helpers for one-time operations.
- Avoid backwards-compatibility shims unless explicitly required.

### File naming

- Use `kebab-case` for filenames unless the language ecosystem mandates something else (e.g., Python `snake_case.py`, Java `PascalCase.java`).
- Configuration files go in the project root or a dedicated `config/` directory.

### Documentation

- Update `README.md` whenever the public interface or setup steps change.
- Update `CLAUDE.md` whenever project structure, conventions, or workflows change.
- Do not create additional Markdown documentation files unless explicitly requested.

### Security

- Never commit secrets, credentials, API keys, or `.env` files.
- Validate only at system boundaries (user input, external APIs); trust internal invariants.
- Avoid common OWASP Top 10 vulnerabilities: SQL injection, XSS, command injection, etc.

## License

Apache License, Version 2.0. All contributions must be compatible with this license. See `LICENSE` for the full text.

## AI Assistant Notes

- **Read before editing:** Always read a file before modifying it.
- **Minimal changes:** Make only the changes that are directly requested or clearly necessary.
- **No time estimates:** Do not predict how long tasks will take.
- **No emojis** unless the user explicitly asks for them.
- **Branch discipline:** All work must land on the designated `claude/` branch; never push to `main` directly.
- **Verify structure:** If new languages, frameworks, or toolchains are introduced, add their build/test/lint commands to this file under a new section.
