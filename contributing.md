---

## ✅ `CONTRIBUTING.md`
# 🤝 Contributing to AWS Unused Tracker

Thank you for your interest in contributing to **AWS Unused Resource Tracker** — a CLI tool to detect and report idle EC2, EBS, and ELB resources to reduce AWS costs.

We welcome all contributions — whether it's a bug fix, feature enhancement, documentation update, or simply feedback!

---

## 📋 How to Contribute

### 1. Fork the Repo

Click the **Fork** button on the top-right of [this repository](https://github.com/Chirag0401/aws-unused-tracker) and clone your copy:

```bash
git clone https://github.com/your-username/aws-unused-tracker.git
cd aws-unused-tracker
```

### 2. Create a New Branch

```bash
git checkout -b your-feature-name
```

### 3. Make Your Changes

Be sure to:
- Follow the existing code style
- Add or update docstrings where needed
- Test your changes locally

### 4. Commit and Push

```bash
git add .
git commit -m "✨ Brief description of your change"
git push origin your-feature-name
```

### 5. Open a Pull Request

Go to your fork on GitHub and click **"Compare & Pull Request"**. Describe what you’ve changed and why.

---

## ✅ Code Guidelines

- Use **Python 3.6+**
- Keep functionality modular and testable
- Avoid hardcoding regions or credentials
- Follow [PEP8](https://peps.python.org/pep-0008/) style guide

---

## 📁 Directory Structure

```
aws_unused_tracker/
├── cli.py               # CLI entry point
├── cost_estimator.py    # Cost Explorer logic
├── ebs_analyzer.py      # EBS idle checks
├── elb_analyzer.py      # ELB request count logic
├── report_generator.py  # JSON/CSV/table exporter
├── resource_fetcher.py  # Region/resource discovery
```

---

## 🧪 Testing (Optional but Encouraged)

We’d love contributions with tests!  
You can use `unittest` or `pytest`.  
(We'll soon add test coverage workflows.)

---

## 💡 Ideas You Can Work On

- [ ] Add unit tests for EC2 + EBS analyzers
- [ ] Add support for tagging idle resources
- [ ] Add Slack/Email alert output
- [ ] Add region filter to output exports
- [ ] Add HTML dashboard export

---

## 🛟 Need Help?

Open an [issue](https://github.com/Chirag0401/aws-unused-tracker/issues) or comment in your pull request.  
We're here to help!

---

## 🫶 Thank You

We appreciate your time and effort in helping this tool grow.  
You're not just optimizing AWS costs — you're building open source with impact!

—
**Chirag Sharma**
```

---

## ✅ Next Step

Save this as `CONTRIBUTING.md` in your root folder:

```bash
cd ~/Project
nano CONTRIBUTING.md
# Paste the content and save
git add CONTRIBUTING.md
git commit -m "📄 Add CONTRIBUTING.md"
git push origin main
```
