# Contributing to OpenClaw Node Manager

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs
- Use the [GitHub Issues](../../issues) page
- Include your OS, Python version, and steps to reproduce
- Attach relevant error messages or console output

### Suggesting Features
- Open an [Issue](../../issues) with the `enhancement` label
- Describe the use case and expected behavior

### Submitting Pull Requests

1. **Fork** the repository and clone your fork
2. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```
3. **Make your changes** following the style guide below
4. **Test** that `server.py` still starts correctly and the UI loads
5. **Commit** with a clear message (see commit convention below)
6. **Push** to your fork and open a Pull Request

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add dark mode toggle
fix: resolve config not saving on Windows
docs: update API reference table
refactor: simplify provider test logic
style: fix button alignment in modal
```

## Code Style

### Python (`server.py`)
- Python 3.6+ compatible syntax
- **No third-party imports** — standard library only
- Use docstrings for functions
- Keep HTTP handlers readable and well-commented

### JavaScript / React (`index.html`)
- React functional components with hooks
- Consistent JSX formatting
- Comment non-obvious logic in Chinese or English

## Development Setup

```bash
# Backend only (simplest)
python server.py

# Full development with hot reload
cd manager-ui
npm install
npm run dev
```

## Questions?

Open an [Issue](../../issues) — we're happy to help!
