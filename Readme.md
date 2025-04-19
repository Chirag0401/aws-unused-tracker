---

## ✅ Here's Your Ready-to-Use `README.md`

```markdown
# 🧹 AWS Unused Resource Tracker

A CLI tool to **track and report unused AWS resources** across EC2 instances, EBS volumes, and ELBs — helping you identify cloud waste and **optimize AWS costs** 💸.

---

## 📸 Output Preview

> _(Insert your screenshot here)_

![CLI Output](./screenshot.png)

---

## 🚀 Features

- 🔍 Scan **EC2, EBS, and ELB** resources for underutilization
- 📊 Check CPU, network, and IOPS metrics via CloudWatch
- 🧮 Estimate monthly **cost savings** using AWS Cost Explorer
- 📁 Export reports to **CSV / JSON**
- ✅ Supports **dry-run** mode for safe preview
- 🌎 Multi-region support via `--region`

---

## 📦 Installation

### 1. Clone the repo:

```bash
git clone https://github.com/your-username/aws-unused-tracker.git
cd aws-unused-tracker
```

### 2. Install as CLI:

```bash
pip install .
```

Now use it anywhere as:

```bash
aws-unused-tracker
```

---

## ⚙️ Usage

```bash
aws-unused-tracker [OPTIONS]
```

### 🔧 Common Flags:

| Option              | Description                                  |
|---------------------|----------------------------------------------|
| `--region`          | Specify one or more AWS regions              |
| `--idle-only`       | Show only idle resources                     |
| `--format`          | Output format: `table`, `json`, `csv`, `all`|
| `--dry-run`         | Preview only, no export or cost lookup      |

### ✅ Examples

```bash
# Show all resources in all regions
aws-unused-tracker

# Scan ap-south-1 only, table format
aws-unused-tracker --region ap-south-1 --format table

# Show only idle EC2/EBS/ELB resources
aws-unused-tracker --idle-only

# Run in dry-run mode (no file writes)
aws-unused-tracker --dry-run
```

---

## 🔐 Required IAM Permissions

To run this tool, the user/role needs read-only permissions like:

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

### 💡 Optional (for cost estimates):

```json
{
  "Effect": "Allow",
  "Action": "ce:GetCostAndUsage",
  "Resource": "*"
}
```

Also ensure [Cost Explorer is enabled](https://console.aws.amazon.com/cost-reports/home?#/settings) in the account.

---

## 📁 Outputs

Reports are saved in the `/output` folder as:

- `ec2_idle_report.json / .csv`
- `ebs_idle_report.json / .csv`
- `elb_idle_report.json / .csv`

---

## 📌 Roadmap

- [ ] Slack/email alerts for idle resources
- [ ] Auto snapshot & stop (opt-in)
- [ ] Tag compliance auditing
- [ ] Multi-account cross-org mode

---

## 👨‍💻 Author

**Your Name**  
GitHub: [@your-username](https://github.com/your-username)  
Feel free to open issues or contribute!

---

## 📄 License

MIT License — Use freely with credit. Contributions welcome 🙌
```

---

