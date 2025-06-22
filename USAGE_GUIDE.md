# Enhanced WELSH-Founder Hunter - Complete Usage Guide

## 🚀 Quick Start for Real Investigation

### 1. Get Your Hiro API Key (Recommended)
```bash
# Visit https://www.hiro.so/hiro-platform to get your free API key
# Benefits: 5000 req/hour vs 500 req/hour without key
export HIRO_API_KEY="your_api_key_here"
```

### 2. Find Real Target Addresses

#### WELSH Contract Address
```bash
# You need the actual deployed WELSH contract address
# Format: SP[39_characters].contract-name
WELSH_CONTRACT="SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token"
```

#### Arkadiko Operational Addresses
```bash
# Known Arkadiko protocol addresses
ARKADIKO_WALLETS=(
    "SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR"  # Main protocol
    "SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE"  # Operations
    # Add more confirmed Arkadiko addresses
)
```

### 3. Run Enhanced Investigation

#### Option A: Command Line (Recommended)
```bash
python cli_tool.py \
  --welsh-contract $WELSH_CONTRACT \
  --arkadiko-wallets "${ARKADIKO_WALLETS[@]}" \
  --output enhanced_investigation.md \
  --verbose
```

#### Option B: Python Script
```python
from enhanced_hunter import EnhancedWELSHFounderHunter

# Configuration with API key
config = {
    'hiro_api_key': 'your_api_key_here',
    'max_cluster_size': 200,
    'analysis_depth': 5,
    'comprehensive_analysis': True
}

# Initialize enhanced hunter
hunter = EnhancedWELSHFounderHunter(config)

# Run comprehensive investigation
result = hunter.run_comprehensive_investigation(
    welsh_contract="SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token",
    arkadiko_wallets=["SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR"]
)

print(f"Investigation complete!")
print(f"Deployer: {result['deployer_address']}")
print(f"Risk Score: {result['deployer_risk_score']:.2f}")
print(f"API Calls Made: {result['api_calls_made']}")
```

#### Option C: REST API
```bash
# Start the API server
python api_wrapper.py

# Submit investigation
curl -X POST "http://localhost:8000/investigate" \
  -H "Content-Type: application/json" \
  -d '{
    "welsh_contract": "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token",
    "arkadiko_wallets": ["SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR"],
    "config_overrides": {
      "hiro_api_key": "your_api_key_here",
      "comprehensive_analysis": true
    }
  }'

# Get results
curl "http://localhost:8000/investigate/{investigation_id}"
```

## 🔍 Enhanced Capabilities Utilized

### Comprehensive Hiro API Endpoints Used

#### Blockchain Status & Info
- `/extended/v1/status` - Chain tip, network info
- `/v2/info` - Network details
- `/v2/pox` - Proof of Transfer info
- `/extended/v1/fee_rate` - Current fee rates

#### Contract Analysis
- `/extended/v1/contract/{contract_id}` - Contract details
- `/extended/v1/contract/{contract_id}/source` - Source code
- `/extended/v1/contract/{contract_id}/interface` - ABI/Interface
- `/extended/v1/contract/{contract_id}/events` - Contract events

#### Transaction Analysis
- `/extended/v1/tx/{tx_id}` - Transaction details
- `/extended/v1/tx/{tx_id}/events` - Transaction events
- `/extended/v1/address/{address}/transactions` - Address history
- `/extended/v1/tx/mempool` - Mempool transactions

#### Address Analysis
- `/extended/v1/address/{address}/stx` - STX balance
- `/extended/v1/address/{address}/nonces` - Nonce information
- `/extended/v1/address/{address}/assets` - All assets
- `/extended/v1/tokens/ft/holdings/{address}` - Fungible tokens
- `/extended/v1/tokens/nft/holdings/{address}` - NFTs

#### Block Analysis
- `/extended/v1/block/{block}` - Block information
- `/extended/v1/block/{block}/transactions` - Block transactions

### Advanced Pattern Detection

#### Transaction Patterns
- **Fee Analysis**: Average, variance, consistency patterns
- **Timing Analysis**: Regular intervals, burst activity, time-of-day patterns
- **Amount Analysis**: Round numbers, amount diversity, large transactions
- **Nonce Analysis**: Sequential patterns, gaps, wallet management indicators

#### Behavioral Analysis
- **Activity Classification**: Low/Medium/High/Very High volume
- **Service Classification**: Exchange, DeFi, Individual, Automated Service
- **Risk Assessment**: Suspicious patterns, money laundering indicators
- **Temporal Analysis**: Active periods, consistency, dormancy patterns

#### Advanced Heuristics
- **Common Input Ownership**: Multiple inputs in same transaction
- **Round Number Transfers**: Internal wallet movements
- **Timing Correlation**: Transactions within minutes
- **Fee Pattern Similarity**: Identical fee strategies
- **Nonce Gap Analysis**: Wallet management patterns

## 📊 Investigation Output

### Comprehensive Report Includes

#### Executive Summary
- Investigation target and date
- Overall confidence score
- Final conclusion
- Key risk factors

#### Deployer Analysis
- Complete address profile
- Transaction history analysis
- Risk assessment
- Service classification
- Activity patterns

#### Technical Evidence
- Blockchain proof data
- Transaction correlation
- Pattern analysis results
- API call statistics

#### Advanced Metrics
- Cluster confidence scores
- Evidence correlation matrix
- Risk factor breakdown
- Temporal analysis

### Sample Output
```markdown
# Enhanced WELSH Token Founder Investigation

## Executive Summary
**Target:** WELSH Token Founder Identity
**Confidence:** 87.3%
**Conclusion:** Probable founder identified
**Risk Level:** Medium

## Deployer Analysis
**Address:** SP1ABC...
**Activity Level:** High (1,247 transactions)
**Risk Score:** 0.65
**Service Type:** Individual suspected
**First Seen:** 2023-08-15
**Last Seen:** 2024-01-15

## Key Evidence
- CEX funding from Binance (confidence: 0.95)
- Arkadiko contract interactions (3 instances)
- Suspicious timing patterns detected
- Round number transaction frequency: 78%

## Technical Metrics
- API calls made: 247
- Addresses analyzed: 23
- Patterns detected: 15
- Evidence items: 12
```

## ⚡ Performance Optimization

### Rate Limiting Strategy
- **With API Key**: 5000 requests/hour
- **Without API Key**: 500 requests/hour
- **Intelligent Backoff**: Automatic retry with exponential backoff
- **Endpoint Switching**: Automatic failover to backup endpoints

### Batch Processing
- Transaction history retrieved in 50-tx batches
- Parallel analysis of multiple addresses
- Efficient caching of analyzed data
- Progressive disclosure of results

### Memory Management
- Streaming analysis for large datasets
- Garbage collection of processed data
- Efficient graph storage
- Compressed evidence storage

## 🔒 Security & Compliance

### Data Handling
- **Read-Only Operations**: No signing or wallet access required
- **Public Data Only**: Uses only publicly available blockchain data
- **No PII Collection**: Addresses are pseudonymous
- **Audit Trail**: Complete logging of all operations

### Legal Considerations
- **Investigative Tool**: For research and analysis only
- **Not Legal Proof**: Results require additional verification
- **Compliance Ready**: Structured for legal review
- **Evidence Chain**: Blockchain-verifiable proof trail

## 🛠 Troubleshooting

### Common Issues

#### API Rate Limiting
```bash
# Solution: Get API key or reduce analysis depth
export HIRO_API_KEY="your_key"
# Or reduce scope
python cli_tool.py --analysis-depth 2 --max-cluster-size 50
```

#### Invalid Addresses
```bash
# Validate Stacks address format
# Must be 41 characters starting with SP or SM
SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9  # Valid
```

#### Network Connectivity
```bash
# Test API connectivity
curl https://api.mainnet.hiro.so/extended/v1/status
```

#### Memory Issues
```bash
# Reduce analysis scope for large investigations
python cli_tool.py --max-cluster-size 100 --analysis-depth 3
```

### Debug Mode
```bash
# Enable verbose logging
python cli_tool.py --verbose --debug

# Check API call statistics
python -c "
from enhanced_hunter import EnhancedWELSHFounderHunter
hunter = EnhancedWELSHFounderHunter({'hiro_api_key': 'your_key'})
print(f'Rate limit: {hunter.api.rate_limit}')
"
```

## 🎯 Advanced Usage

### Custom Configuration
```python
config = {
    'hiro_api_key': 'your_key',
    'max_cluster_size': 500,           # Larger clusters
    'analysis_depth': 10,              # Deeper analysis
    'confidence_threshold': 85,        # Higher threshold
    'comprehensive_analysis': True,    # Full analysis
    'temporal_correlation_window': 7200,  # 2-hour window
    'evidence_correlation_minimum': 0.7   # Higher correlation
}
```

### Batch Investigation
```python
# Investigate multiple contracts
contracts = [
    "SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token",
    "SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR.other-token"
]

for contract in contracts:
    result = hunter.run_comprehensive_investigation(
        welsh_contract=contract,
        arkadiko_wallets=arkadiko_wallets
    )
    print(f"{contract}: {result['deployer_address']}")
```

### Export Options
```bash
# Multiple output formats
python cli_tool.py --format json --output results.json
python cli_tool.py --format markdown --output report.md
python cli_tool.py --format csv --output data.csv
```

## 📈 Scaling for Production

### High-Volume Analysis
- Use multiple API keys for parallel processing
- Implement Redis caching for analyzed addresses
- Database storage for persistent evidence
- Kubernetes deployment for scalability

### Enterprise Features
- Multi-tenant investigation management
- Role-based access control
- Audit logging and compliance reporting
- Integration with legal case management systems

---

**🚀 Ready to run real investigations with comprehensive Hiro API utilization!**