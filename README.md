# WELSH-Founder Hunter 🔍 - Enhanced Edition

**Autonomous blockchain forensics agent utilizing comprehensive Hiro API capabilities for identifying WELSH token founder through advanced wallet clustering and cross-chain analysis**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Hiro API](https://img.shields.io/badge/Hiro_API-Enhanced-blue.svg)](https://www.hiro.so/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## Overview
WELSH-Founder Hunter is a production-ready blockchain forensics agent designed to autonomously investigate and identify the founder of the WELSH token through sophisticated wallet clustering, comprehensive transaction analysis, and advanced cross-platform correlation techniques utilizing every available Hiro API endpoint.
WELSH-Founder Hunter is a production-ready blockchain forensics agent designed to autonomously investigate and identify the founder of the WELSH token through sophisticated wallet clustering, transaction analysis, and cross-platform correlation techniques.

## Key Features
- **🤖 Fully Autonomous**: 8-phase state machine with comprehensive Hiro API utilization
- **🔍 Advanced Forensics**: Multi-layered analysis using 15+ Hiro API endpoints
- **📊 Enhanced Evidence Scoring**: Advanced correlation algorithms (80%+ = "Probable founder")
- **🌐 Comprehensive API Coverage**: Utilizes contracts, transactions, addresses, blocks, mempool, and network APIs
- **⚡ Intelligent Rate Limiting**: 5000 req/hour with API key, automatic failover
- **🔗 Deep Pattern Analysis**: Advanced behavioral, temporal, and correlation analysis
- **⚖️ Legal Ready**: Blockchain-verifiable evidence with comprehensive audit trails
- **🔒 Security First**: Read-only design with multi-endpoint redundancy
## Mission Phases

| Phase | Objective | Autonomous Actions |
|-------|-----------|-------------------|
| **0** | Bootstrap | Load config, fetch seed addresses |
| **1** | Deployer Discovery | Identify original deploy tx via Hiro API |
| **2** | Wallet-Cluster Expansion | Build 2-hop graph using 4 heuristics |
| **3** | Funding-Source Trace | Follow STX inputs, identify CEX sources |
| **4** | Arkadiko Overlap Scan | Cross-reference with Arkadiko operations |
| **5** | Off-chain Correlation | GitHub/Discord metadata analysis |
| **6** | Evidence Scoring | Weighted confidence calculation |
| **7** | Report Generation | Markdown dossier with Mermaid graphs |

## Evidence Scoring System

- **+40 pts**: Shared CEX withdrawal
- **+25 pts**: Wallet overlap with Arkadiko
- **+15 pts**: Identical fee/nonce patterns
- **+10 pts**: Stylometry matches
- **70%+ confidence** = "Probable founder"

## Quick Start

### 1. Installation

```bash
git clone https://github.com/KidCudi718/welsh-founder-hunter.git
cd welsh-founder-hunter
pip install -r requirements.txt
```

### 2. Configuration

Copy the environment template:
```bash
cp .env.template .env
```

Edit `.env` with your API keys:
```bash
# Required for higher rate limits
HIRO_API_KEY=your_hiro_api_key_here

# Optional for enhanced analysis
DISCORD_BOT_TOKEN=your_discord_bot_token_here
GITHUB_PAT=your_github_personal_access_token_here
```

### 3. Run Investigation

#### Command Line
```bash
python cli_tool.py \
  --welsh-contract SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token \
  --arkadiko-wallets SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR \
  --output investigation_report.md
```

#### Python API
```python
from welsh_hunter import WELSHFounderHunter, create_welsh_hunter_config

# Initialize
config = create_welsh_hunter_config()
hunter = WELSHFounderHunter(config)

# Run investigation
result = hunter.run_full_investigation(
    welsh_contract="SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token",
    arkadiko_wallets=["SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR"]
)

print(f"Conclusion: {result['conclusion']}")
print(f"Confidence: {result['confidence_score']:.1f}%")
```

#### REST API
```bash
# Start API server
python api_wrapper.py

# Submit investigation
curl -X POST "http://localhost:8000/investigate" \
  -H "Content-Type: application/json" \
  -d '{
    "welsh_contract": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token",
    "arkadiko_wallets": ["SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR"]
  }'

# Get results
curl "http://localhost:8000/investigate/{investigation_id}"
```

## Docker Deployment

```bash
# Build image
docker build -t welsh-founder-hunter .

# Run container
docker run -p 8000:8000 \
  -e HIRO_API_KEY=your_key_here \
  welsh-founder-hunter
```

## Agent Platform Deployment

### Softgen/LangGraph
```yaml
# Use softgen-config.yaml
agent_name: welsh-founder-hunter
runtime: python3.11
workflow:
  entrypoint: bootstrap
```

### SuperAgent
```json
{
  "name": "welsh-founder-hunter",
  "type": "blockchain-forensics",
  "runtime": "python3.11",
  "entry_point": "welsh_hunter.py"
}
```

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Plane    │    │ Graph Analytics │    │ Off-chain APIs  │
│                 │    │                 │    │                 │
│ • Hiro Stacks   │    │ • NetworkX      │    │ • Discord Bot   │
│ • Stacks.js     │    │ • Neo4j         │    │ • GitHub API    │
│ • Raw RPC       │    │ • Clustering    │    │ • Medium RSS    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ WELSH-Founder   │
                    │    Hunter       │
                    │                 │
                    │ • State Machine │
                    │ • Evidence DB   │
                    │ • Report Gen    │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │    Outputs      │
                    │                 │
                    │ • Markdown      │
                    │ • JSON Data     │
                    │ • PDF Reports   │
                    │ • Subpoena Docs │
                    └─────────────────┘
```

## Required Access & Credentials

| Access | Purpose | How to Provision |
|--------|---------|------------------|
| **Hiro API Key** | Higher rate limits | Free at [hiro.so](https://hiro.so) |
| **Discord Bot Token** | Channel analysis | Discord Developer Portal |
| **GitHub PAT** | Repo analysis | GitHub Settings → Developer |
| **CEX Tag Database** | Exchange identification | Import CSV or API |
| **AWS S3** | Evidence storage | IAM user with S3 access |

## Legal & Compliance

- **🔒 Read-only**: No signing privileges required
- **⚖️ Legal hooks**: Subpoena template generation
- **📋 Audit trail**: Complete evidence logging
- **🛡️ Privacy**: No PII collection
- **⚠️ Disclaimer**: Not definitive legal proof

## What the Agent Cannot Do

1. **Compel KYC disclosures** - requires legal subpoena
2. **Force public statements** - needs social engineering
3. **Legal interpretation** - requires counsel review

Everything else is fully automated.

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
black welsh_hunter.py
flake8 welsh_hunter.py
mypy welsh_hunter.py
```

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## Examples

### Basic Investigation
```python
hunter = WELSHFounderHunter(config)
result = hunter.run_full_investigation(
    welsh_contract="SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token",
    arkadiko_wallets=["SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR"]
)
```

### Advanced Configuration
```python
config = {
    'hiro_api_key': 'your_key',
    'max_cluster_size': 100,
    'analysis_depth': 3,
    'confidence_threshold': 80,
    'subpoena_mode': True
}
```

## Output Examples

### Investigation Report
```markdown
# WELSH Token Founder Investigation Report

## Executive Summary
**Confidence Score:** 85.2%
**Conclusion:** Probable founder

## Key Findings
- Deployer: SP1ABC...
- Cluster size: 23 addresses
- CEX funding: 3 instances
- Arkadiko overlap: High correlation
```

### JSON Results
```json
{
  "success": true,
  "confidence_score": 85.2,
  "conclusion": "Probable founder",
  "deployer_address": "SP1ABC...",
  "cluster_size": 23,
  "evidence_count": 15
}
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/KidCudi718/welsh-founder-hunter/issues)
- **Documentation**: [Wiki](https://github.com/KidCudi718/welsh-founder-hunter/wiki)
- **Security**: Report to security@example.com

---

**⚠️ Legal Disclaimer**: This tool is for investigative purposes only. Results should not be considered definitive legal proof. Always consult legal counsel before taking action based on these findings.

**🔍 Ready for production deployment on any agent platform!**