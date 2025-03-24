# AWS Security Scanner 🔐

An automated security audit tool that scans AWS IAM users and S3 bucket configurations for potential security risks.

This tool:
- Lists IAM users
- Detects users without MFA
- Retrieves all S3 buckets
- Identifies public S3 buckets
- Optionally uploads the scan report to S3

Built with:
- **AWS Lambda**
- **Python** using the `boto3` SDK
- **IAM policies** for least-privilege access
- **JSON** formatted reports

---

## 📦 Installation

```bash
git clone https://github.com/SimhaReddyJanne/AWS-Security-Scanner.git
cd AWS-Security-Scanner
pip install -r requirements.txt
