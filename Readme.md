## ✅ `README.md`

```markdown
# 🧹 AWS Unused Resource Tracker

A CLI tool to **track and report unused AWS resources** across EC2 instances, EBS volumes, and ELBs — helping you identify cloud waste and **optimize AWS costs** 💸.

---

## 📸 Output Preview

> _(Insert your screenshot below)_

![CLI Output](./screenshot.png)

---

## 🚀 Features

- 🔍 Scan **EC2, EBS, and ELB** resources for underutilization
- 📊 Analyze usage with CloudWatch metrics (CPU, network, IOPS)
- 🧮 Estimate monthly **cost savings** via AWS Cost Explorer
- 📁 Export results to **CSV / JSON**
- ✅ Use `--dry-run` to preview without exporting or costing
- 🌍 Multi-region support

---

## 📦 Installation

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/aws-unused-tracker.git
cd aws-unused-tracker
```

### 2. Install as a CLI tool:

```bash
pip install .
```

### ✅ Usage

```bash
aws-unused-tracker [OPTIONS]
```

---

## ⚙️ CLI Options

| Option              | Description                                  |
|---------------------|----------------------------------------------|
| `--region`          | Specify one or more AWS regions              |
| `--idle-only`       | Show only idle resources                     |
| `--format`          | Output format: `table`, `json`, `csv`, `all`|
| `--dry-run`         | Preview only, no export or cost estimation  |

---

## 💡 Examples

```bash
# Scan all regions, output to terminal
aws-unused-tracker --format table

# Scan ap-south-1, only show idle
aws-unused-tracker --region ap-south-1 --idle-only

# Dry-run mode (no files or billing data)
aws-unused-tracker --dry-run
```

---

## 🔐 Required IAM Permissions

Minimum read-only permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:DescribeInstances",
    "ec2:DescribeVolumes",
    "elasticloadbalancing:DescribeLoadBalancers",
    "cloudwatch:GetMetricStatistics"
  ],
  "Resource": "*"
}
```

**Optional for cost savings estimate:**

```json
{
  "Effect": "Allow",
  "Action": "ce:GetCostAndUsage",
  "Resource": "*"
}
```

👉 Also ensure **Cost Explorer is enabled** in your AWS Billing settings.

---

## 📁 Output Files

By default, output is saved to the `/output` directory:

- `ec2_idle_report.json` / `.csv`
- `ebs_idle_report.json` / `.csv`
- `elb_idle_report.json` / `.csv`

---

## 🛣 Roadmap

- [ ] Slack/email notifications for idle resources
- [ ] Resource tag compliance check
- [ ] Multi-account org-wide support

---

## 👨‍💻 Author

**Chirag Sharma**  
GitHub: [@Chirag0401](https://github.com/Chirag0401)

> Feel free to star ⭐ the repo, submit issues, or contribute!

---

## 📄 License

Licensed under the [MIT License](LICENSE).  
Use it freely, improve it proudly, contribute generously 🙌
```

---

Once you add your `screenshot.png` file next to this, GitHub will render it beautifully.

Let me know if you'd like me to:
- Add badges (stars, license, version, Python)
- Help prep for PyPI publishing next!
