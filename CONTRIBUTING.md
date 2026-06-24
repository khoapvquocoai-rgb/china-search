# Contributing to China Search Skill

Thank you for your interest in contributing! This document provides guidelines to help you contribute effectively.

---

## 🎯 How to Contribute

### 1. Report Bugs

**Before creating bug reports:**
- Check existing issues to avoid duplicates
- Update to latest version to see if bug is fixed
- Gather error messages and reproduction steps

**Creating bug reports:**
```markdown
### Bug Report Template

**Description:**
Clear, concise description of the bug

**Steps to Reproduce:**
1. Go to '...'
2. Run command '....'
3. Click on '....'
4. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happened

**Environment:**
- Dify version: [e.g., 0.6.0]
- Python version: [e.g., 3.10]
- OS: [e.g., macOS 14.0]
- Hardware: [optional, e.g., M1 Mac]

**Additional Context:**
- Screenshots if UI-related
- Log files if available
- Sample input that triggers the bug

**Possible Fix (Optional):**
If you know how to fix it
```

### 2. Suggest Features

**Before suggesting features:**
- Check if feature already exists or is in progress
- Consider if it aligns with project goals (zero-budget, lawful research)
- Think about security implications

**Feature request template:**
```markdown
### Feature Request

**Problem Statement:**
What problem does this solve?

**Proposed Solution:**
How should it work?

**Alternatives Considered:**
Other approaches you've thought about

**Use Case:**
Real-world scenario where this would help

**Security Considerations:**
Any risks or privacy concerns?
```

### 3. Translate Content

We need help translating prompts and documentation to:
- Simplified Chinese (中文简体)
- Traditional Chinese (繁體中文)
- Other languages

**Translation guidelines:**
- Keep technical terms in English when appropriate
- Preserve Jinja2 template syntax (`{{ }}`, `{% %}`)
- Maintain prompt structure and logic
- Add translator credit in comments

**Process:**
1. Fork repo
2. Create `translations/<language>/` directory
3. Add translated files
4. Update `SKILL.md` with language support note
5. Submit PR

### 4. Improve Documentation

Areas needing improvement:
- More concrete examples
- Diagrams for complex workflows
- Troubleshooting guides
- Video tutorials
- Real-world case studies

**Documentation standards:**
- Use Markdown
- Include code examples
- Add screenshots where helpful
- Link to related docs
- Test all commands before submitting

### 5. Submit Code Changes

**Development workflow:**

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/china-search.git
cd china-search

# 2. Create branch
git checkout -b feature/your-feature-name

# 3. Make changes
# Edit files, add tests, update docs

# 4. Test thoroughly
python scripts/generate_workflow_json.py --project "Test" --output test.json
python -m py_compile scripts/*.py  # Syntax check

# 5. Commit
git add .
git commit -m "feat: add your feature description"

# 6. Push and create PR
git push origin feature/your-feature-name
```

**Commit message conventions:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## 📋 Development Guidelines

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Keep functions under 50 lines when possible

**Example:**
```python
def generate_search_matrix(query: str, entity: str = "") -> list[dict]:
    """
    Generate search matrix for Chinese queries.
    
    Args:
        query: Main search topic
        entity: Optional specific entity
        
    Returns:
        List of query dictionaries with source URLs
    """
    # Implementation here
    pass
```

**Markdown:**
- Use consistent heading levels
- Include table of contents for long docs
- Add links between related sections
- Use code blocks for commands

### Testing Requirements

Before submitting:

1. **Syntax check:**
   ```bash
   python -m py_compile scripts/*.py
   ```

2. **Run example:**
   ```bash
   python scripts/generate_workflow_json.py --project "Test" --output /tmp/test.json
   cat /tmp/test.json | python -m json.tool  # Validate JSON
   ```

3. **Test edge cases:**
   - Empty inputs
   - Very long queries
   - Special characters
   - Unicode (Chinese characters)

4. **Update docs:**
   - Reflect new features
   - Add examples
   - Update version history

### Security Review

All contributions must pass security review:

- ✅ No hardcoded API keys or secrets
- ✅ Input validation on user data
- ✅ Safe file handling (no path traversal)
- ✅ Proper error handling (no stack traces exposed)
- ✅ Compliance with CAC regulations mentioned

**Questions?** Ask maintainers during PR review.

---

## 🏷️ Issue and PR Labels

| Label | Description |
|-------|-------------|
| `bug` | Confirmed bug |
| `enhancement` | New feature request |
| `documentation` | Docs improvement |
| `good first issue` | Beginner-friendly |
| `help wanted` | Needs community help |
| `security` | Security-related |
| `translation` | Translation task |
| `wontfix` | Won't be addressed |

---

## 🤝 Code of Conduct

### Our Pledge

We pledge to make participation in our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

**Unacceptable behavior:**
- Sexualized language or imagery
- Trolling or insulting comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information

### Enforcement

Violations may be reported to maintainers. All complaints will be reviewed and investigated promptly.

---

## 📚 Resources for Contributors

### Learning Materials

- [Dify Documentation](https://docs.dify.ai) - Understand platform capabilities
- [Jinja2 Templates](https://jinja.palletsprojects.com/) - Learn templating syntax
- [Python Best Practices](https://realpython.com/python-pep8/) - Code style guide
- [Markdown Guide](https://www.markdownguide.org/) - Documentation formatting

### Tools

- **Pre-commit hooks:** Run automatically before commits
- **Linting:** `flake8`, `black` for Python
- **Testing:** `pytest` framework
- **Docs preview:** Local markdown rendering

### Getting Help

- **Discussions:** Use GitHub Discussions for questions
- **Issues:** For bugs and feature requests
- **Maintainers:** Tag @khoapvquocoai-rgb for urgent matters

---

## 🎉 Your First Contribution

### Easy First Steps

1. **Fix typos** in documentation
2. **Add examples** to existing templates
3. **Translate** a section to another language
4. **Improve error messages** in scripts
5. **Add test cases** for edge scenarios

### Process

1. Find an issue labeled `good first issue`
2. Comment "I'd like to work on this"
3. Wait for maintainer assignment
4. Follow development guidelines above
5. Submit PR and wait for review

---

## ⏱️ Response Time

We aim to:
- Acknowledge issues within 48 hours
- Review PRs within 1 week
- Respond to questions within 3 days

*Note: Maintainers are volunteers. Patience appreciated!*

---

## 🙏 Thank You!

Every contribution matters, no matter how small. Thank you for helping make china-search better for everyone!

**Questions?** Open an issue or discussion - we're happy to help!

---

<div align="center">

**Ready to contribute?** [Find a good first issue](https://github.com/khoapvquocoai-rgb/china-search/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)

</div>
