# Automated-Cloud-Security-Guardrails

# 🔐 Automated Cloud Security Guardrails (Self-Healing AWS Security)

This project implements automated security guardrails on AWS that detect insecure configuration changes in real time and automatically remediate them.

## 🚀 Features
- Detects public S3 buckets and blocks public access
- Detects open SSH (0.0.0.0/0:22) in Security Groups and auto-revokes the rule
- Sends real-time alerts via SNS email
- Fully serverless and event-driven

## 🧱 Architecture
AWS Config → EventBridge → Lambda (Auto-Remediation) → SNS (Alert)

## 🛠️ AWS Services Used
- AWS Config
- EventBridge
- Lambda
- SNS
- IAM

## 📸 Demo Screenshots
Screenshots are available in the `/screenshots` folder.

## 🧪 How to Test
1. Make an S3 bucket public → it will auto-lock
2. Open SSH to 0.0.0.0/0 → it will auto-close
