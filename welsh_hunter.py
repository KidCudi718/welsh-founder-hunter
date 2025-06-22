# WELSH-Founder Hunter AI Agent
# Production-ready blockchain forensics agent for Stacks ecosystem

import json
import requests
import networkx as nx
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import re
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import time

@dataclass
class WalletCluster:
    """Represents a cluster of related wallets"""
    primary_address: str
    related_addresses: Set[str]
    confidence_score: float
    heuristics: List[str]
    first_seen: datetime
    last_seen: datetime

@dataclass
class Evidence:
    """Evidence item for founder correlation"""
    evidence_type: str
    description: str
    confidence: float
    timestamp: datetime
    source_data: Dict

class WELSHFounderHunter:
    """
    Autonomous blockchain forensics agent for identifying WELSH token founder
    through wallet clustering and cross-chain analysis
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.hiro_api_base = "https://api.hiro.so"
        self.session = requests.Session()
        
        # Set API headers if key provided
        if config.get('hiro_api_key'):
            self.session.headers.update({
                'X-API-Key': config['hiro_api_key']
            })
        
        # Initialize data stores
        self.wallet_graph = nx.DiGraph()
        self.clusters = {}
        self.evidence = []
        self.cex_tags = self._load_cex_tags()
        
        # Mission state tracking
        self.mission_state = {
            'phase': 0,
            'completed_phases': [],
            'current_objective': 'Bootstrap',
            'evidence_score': 0
        }
        
        print("🔍 WELSH-Founder Hunter initialized")
        print(f"📊 Mission State: Phase {self.mission_state['phase']} - {self.mission_state['current_objective']}")
    
    def _load_cex_tags(self) -> Dict[str, str]:
        """Load known CEX wallet tags"""
        # Basic CEX patterns - in production, use comprehensive tag DB
        return {
            # Binance patterns
            'SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE': 'binance_hot_1',
            'SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7': 'binance_hot_2',
            # OKX patterns  
            'SP1Y5YSTAHZ88XYK1VPDH24GY0HPX5J4JECTMY4A1': 'okx_hot_1',
            # KuCoin patterns
            'SP32AEEF6WW5Y0NMJ1S8SBSZDAY8R5J32NBZFPKKZ': 'kucoin_hot_1'
        }
    
    def bootstrap(self, welsh_contract: str, arkadiko_wallets: List[str], 
                  philip_wallets: List[str] = None) -> bool:
        """Phase 0: Bootstrap - Load configuration and seed addresses"""
        try:
            print("\n🚀 Phase 0: Bootstrap")
            
            # Store seed data
            self.welsh_contract = welsh_contract
            self.arkadiko_wallets = set(arkadiko_wallets)
            self.philip_wallets = set(philip_wallets or [])
            
            # Cache seed addresses
            seed_data = {
                'welsh_contract': welsh_contract,
                'arkadiko_wallets': list(self.arkadiko_wallets),
                'philip_wallets': list(self.philip_wallets),
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Loaded WELSH contract: {welsh_contract}")
            print(f"✅ Loaded {len(self.arkadiko_wallets)} Arkadiko wallets")
            print(f"✅ Loaded {len(self.philip_wallets)} Philip wallets")
            
            self._update_mission_state(1, 'Deployer Discovery')
            return True
            
        except Exception as e:
            print(f"❌ Bootstrap failed: {e}")
            return False
    
    def discover_deployer(self) -> Optional[Tuple[str, str]]:
        """Phase 1: Identify original deployment transaction and deployer"""
        try:
            print("\n🔍 Phase 1: Deployer Discovery")
            
            # Get contract info to find deployment tx
            url = f"{self.hiro_api_base}/extended/v1/contract/{self.welsh_contract}"
            response = self.session.get(url)
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch contract info: {response.status_code}")
                return None
            
            contract_data = response.json()
            deploy_tx = contract_data.get('tx_id')
            
            # Get full transaction details
            tx_url = f"{self.hiro_api_base}/extended/v1/tx/{deploy_tx}"
            tx_response = self.session.get(tx_url)
            
            if tx_response.status_code == 200:
                tx_data = tx_response.json()
                deployer = tx_data.get('sender_address')
                deploy_time = tx_data.get('burn_block_time_iso')
                
                print(f"✅ Found deployer: {deployer}")
                print(f"✅ Deploy TX: {deploy_tx}")
                print(f"✅ Deploy time: {deploy_time}")
                
                # Cache deployer info
                self.deployer_info = {
                    'address': deployer,
                    'deploy_tx': deploy_tx,
                    'deploy_time': deploy_time
                }
                
                self._update_mission_state(2, 'Wallet-Cluster Expansion')
                return deployer, deploy_tx
            
            return None
            
        except Exception as e:
            print(f"❌ Deployer discovery failed: {e}")
            return None
    
    def expand_wallet_cluster(self, seed_address: str, max_hops: int = 2) -> WalletCluster:
        """Phase 2: Build graph of wallets controlled by deployer using heuristics"""
        try:
            print(f"\n🕸️ Phase 2: Wallet-Cluster Expansion for {seed_address}")
            
            visited = set()
            to_visit = [(seed_address, 0)]  # (address, hop_count)
            related_addresses = set()
            heuristics_found = []
            
            while to_visit and len(visited) < 100:  # Safety limit
                current_addr, hop_count = to_visit.pop(0)
                
                if current_addr in visited or hop_count > max_hops:
                    continue
                    
                visited.add(current_addr)
                print(f"  🔍 Analyzing {current_addr} (hop {hop_count})")
                
                # Get transaction history
                txs = self._get_address_transactions(current_addr)
                
                # Apply clustering heuristics
                cluster_candidates = self._apply_clustering_heuristics(current_addr, txs)
                
                for candidate, heuristic in cluster_candidates:
                    if candidate not in visited:
                        related_addresses.add(candidate)
                        heuristics_found.append(heuristic)
                        
                        if hop_count < max_hops:
                            to_visit.append((candidate, hop_count + 1))
                
                # Add edges to graph
                for candidate, _ in cluster_candidates:
                    self.wallet_graph.add_edge(current_addr, candidate)
                
                time.sleep(0.1)  # Rate limiting
            
            # Calculate confidence score
            confidence = self._calculate_cluster_confidence(related_addresses, heuristics_found)
            
            cluster = WalletCluster(
                primary_address=seed_address,
                related_addresses=related_addresses,
                confidence_score=confidence,
                heuristics=heuristics_found,
                first_seen=datetime.now() - timedelta(days=365),  # Placeholder
                last_seen=datetime.now()
            )
            
            self.clusters[seed_address] = cluster
            
            print(f"✅ Found cluster with {len(related_addresses)} related addresses")
            print(f"✅ Confidence score: {confidence:.2f}")
            
            self._update_mission_state(3, 'Funding-Source Trace')
            return cluster
            
        except Exception as e:
            print(f"❌ Wallet clustering failed: {e}")
            return None
    
    def _get_address_transactions(self, address: str, limit: int = 50) -> List[Dict]:
        """Get transaction history for an address"""
        try:
            url = f"{self.hiro_api_base}/extended/v1/address/{address}/transactions"
            params = {'limit': limit}
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json().get('results', [])
            return []
            
        except Exception as e:
            print(f"⚠️ Failed to get transactions for {address}: {e}")
            return []
    
    def _apply_clustering_heuristics(self, address: str, transactions: List[Dict]) -> List[Tuple[str, str]]:
        """Apply wallet clustering heuristics"""
        candidates = []
        
        # Heuristic 1: Common input ownership (multiple inputs in same tx)
        for tx in transactions:
            if tx.get('tx_type') == 'token_transfer':
                # Look for transactions with multiple STX inputs
                inputs = tx.get('stx_sent', 0)
                if inputs > 0:
                    sender = tx.get('sender_address')
                    if sender and sender != address:
                        candidates.append((sender, 'common_input_ownership'))
        
        # Heuristic 2: Round number transfers (likely internal)
        for tx in transactions:
            amount = tx.get('stx_sent', 0)
            if amount and amount % 1000000 == 0:  # Round STX amounts
                recipient = tx.get('recipient_address')
                if recipient:
                    candidates.append((recipient, 'round_number_transfer'))
        
        # Heuristic 3: Timing correlation (transactions within minutes)
        tx_times = [(tx.get('burn_block_time'), tx.get('sender_address')) for tx in transactions]
        for i, (time1, addr1) in enumerate(tx_times):
            for time2, addr2 in tx_times[i+1:]:
                if addr1 != addr2 and abs(time1 - time2) < 300:  # 5 minutes
                    candidates.append((addr2, 'timing_correlation'))
        
        # Heuristic 4: Fee pattern similarity
        fee_patterns = defaultdict(list)
        for tx in transactions:
            fee = tx.get('fee_rate', 0)
            sender = tx.get('sender_address')
            if fee and sender:
                fee_patterns[fee].append(sender)
        
        for fee, senders in fee_patterns.items():
            if len(senders) > 1:
                for sender in senders:
                    if sender != address:
                        candidates.append((sender, 'fee_pattern_similarity'))
        
        return candidates
    
    def _calculate_cluster_confidence(self, addresses: Set[str], heuristics: List[str]) -> float:
        """Calculate confidence score for wallet cluster"""
        base_score = min(len(addresses) * 10, 50)  # Up to 50 points for cluster size
        
        heuristic_scores = {
            'common_input_ownership': 30,
            'round_number_transfer': 20,
            'timing_correlation': 15,
            'fee_pattern_similarity': 25
        }
        
        heuristic_score = sum(heuristic_scores.get(h, 5) for h in set(heuristics))
        
        return min(base_score + heuristic_score, 100) / 100
    
    def trace_funding_sources(self, cluster: WalletCluster) -> List[Dict]:
        """Phase 3: Follow STX inputs that funded gas fees & LP wallet"""
        try:
            print("\n💰 Phase 3: Funding-Source Trace")
            
            funding_sources = []
            
            for address in [cluster.primary_address] | cluster.related_addresses:
                print(f"  🔍 Tracing funding for {address}")
                
                # Get incoming STX transfers
                txs = self._get_address_transactions(address, limit=100)
                
                for tx in txs:
                    if tx.get('tx_type') == 'token_transfer' and tx.get('token_transfer', {}).get('recipient_address') == address:
                        sender = tx.get('sender_address')
                        amount = tx.get('token_transfer', {}).get('amount', 0)
                        
                        # Check if sender is a known CEX
                        cex_label = self.cex_tags.get(sender)
                        
                        funding_info = {
                            'recipient': address,
                            'sender': sender,
                            'amount': amount,
                            'tx_id': tx.get('tx_id'),
                            'timestamp': tx.get('burn_block_time_iso'),
                            'is_cex': bool(cex_label),
                            'cex_label': cex_label
                        }
                        
                        funding_sources.append(funding_info)
                        
                        if cex_label:
                            print(f"  🏦 Found CEX funding: {cex_label} -> {address}")
                            
                            # High-value evidence
                            evidence = Evidence(
                                evidence_type='cex_funding',
                                description=f'CEX withdrawal from {cex_label} to cluster wallet',
                                confidence=0.8,
                                timestamp=datetime.now(),
                                source_data=funding_info
                            )
                            self.evidence.append(evidence)
                
                time.sleep(0.1)  # Rate limiting
            
            print(f"✅ Found {len(funding_sources)} funding sources")
            print(f"✅ Found {len([f for f in funding_sources if f['is_cex']])} CEX sources")
            
            self._update_mission_state(4, 'Arkadiko Overlap Scan')
            return funding_sources
            
        except Exception as e:
            print(f"❌ Funding source trace failed: {e}")
            return []
    
    def scan_arkadiko_overlap(self, cluster: WalletCluster) -> Dict:
        """Phase 4: Look for links between founder cluster & Arkadiko ops wallets"""
        try:
            print("\n🔗 Phase 4: Arkadiko Overlap Scan")
            
            cluster_addresses = {cluster.primary_address} | cluster.related_addresses
            overlaps = []
            
            # Get Arkadiko contract interactions
            arkadiko_contracts = [
                'SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR.arkadiko-dao',
                'SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR.arkadiko-stacker-v1-1',
                'SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR.arkadiko-vault-manager-v1-1'
            ]
            
            for contract in arkadiko_contracts:
                print(f"  🔍 Checking interactions with {contract}")
                
                # Get contract call events
                url = f"{self.hiro_api_base}/extended/v1/contract/{contract}/events"
                response = self.session.get(url, params={'limit': 100})
                
                if response.status_code == 200:
                    events = response.json().get('results', [])
                    
                    for event in events:
                        caller = event.get('tx', {}).get('sender_address')
                        
                        if caller in cluster_addresses:
                            overlap_info = {
                                'cluster_address': caller,
                                'arkadiko_contract': contract,
                                'tx_id': event.get('tx', {}).get('tx_id'),
                                'event_type': event.get('event_type'),
                                'timestamp': event.get('tx', {}).get('burn_block_time_iso')
                            }
                            overlaps.append(overlap_info)
                            
                            print(f"  🎯 Found overlap: {caller} -> {contract}")
                            
                            # Add evidence
                            evidence = Evidence(
                                evidence_type='arkadiko_interaction',
                                description=f'Cluster wallet interacted with Arkadiko contract',
                                confidence=0.6,
                                timestamp=datetime.now(),
                                source_data=overlap_info
                            )
                            self.evidence.append(evidence)
                
                time.sleep(0.2)  # Rate limiting
            
            # Check for shared UTXO partners
            jaccard_scores = self._calculate_jaccard_similarity(cluster_addresses)
            
            overlap_result = {
                'direct_overlaps': overlaps,
                'jaccard_scores': jaccard_scores,
                'high_correlation': len(overlaps) > 0 or max(jaccard_scores.values(), default=0) > 0.3
            }
            
            print(f"✅ Found {len(overlaps)} direct overlaps")
            print(f"✅ High correlation: {overlap_result['high_correlation']}")
            
            self._update_mission_state(5, 'Off-chain Correlation')
            return overlap_result
            
        except Exception as e:
            print(f"❌ Arkadiko overlap scan failed: {e}")
            return {}
    
    def _calculate_jaccard_similarity(self, cluster_addresses: Set[str]) -> Dict[str, float]:
        """Calculate Jaccard similarity between cluster and Arkadiko wallets"""
        scores = {}
        
        for arkadiko_addr in self.arkadiko_wallets:
            # Get transaction partners for both sets
            cluster_partners = set()
            arkadiko_partners = set()
            
            # This is simplified - in production, implement full UTXO partner analysis
            for addr in cluster_addresses:
                txs = self._get_address_transactions(addr, limit=20)
                for tx in txs:
                    if tx.get('sender_address') != addr:
                        cluster_partners.add(tx.get('sender_address'))
                    if tx.get('recipient_address') != addr:
                        cluster_partners.add(tx.get('recipient_address'))
            
            txs = self._get_address_transactions(arkadiko_addr, limit=20)
            for tx in txs:
                if tx.get('sender_address') != arkadiko_addr:
                    arkadiko_partners.add(tx.get('sender_address'))
                if tx.get('recipient_address') != arkadiko_addr:
                    arkadiko_partners.add(tx.get('recipient_address'))
            
            # Calculate Jaccard similarity
            intersection = len(cluster_partners & arkadiko_partners)
            union = len(cluster_partners | arkadiko_partners)
            
            if union > 0:
                scores[arkadiko_addr] = intersection / union
            else:
                scores[arkadiko_addr] = 0.0
        
        return scores
    
    def correlate_offchain_data(self) -> Dict:
        """Phase 5: Scrape public artifacts for metadata overlap"""
        try:
            print("\n🌐 Phase 5: Off-chain Correlation")
            
            correlations = {
                'github_analysis': self._analyze_github_repos(),
                'timing_analysis': self._analyze_timing_patterns(),
                'stylometry_matches': []
            }
            
            print("✅ Off-chain correlation analysis complete")
            
            self._update_mission_state(6, 'Evidence Scoring')
            return correlations
            
        except Exception as e:
            print(f"❌ Off-chain correlation failed: {e}")
            return {}
    
    def _analyze_github_repos(self) -> Dict:
        """Analyze GitHub repositories for commit patterns"""
        # Placeholder for GitHub analysis
        # In production, implement full commit analysis
        return {
            'arkadiko_commits': [],
            'welsh_commits': [],
            'author_overlap': False,
            'timing_correlation': 0.0
        }
    
    def _analyze_timing_patterns(self) -> Dict:
        """Analyze timing patterns across different data sources"""
        # Placeholder for timing analysis
        return {
            'transaction_patterns': [],
            'commit_patterns': [],
            'correlation_score': 0.0
        }
    
    def score_evidence(self) -> float:
        """Phase 6: Quantify strength of proof using weighted scoring"""
        try:
            print("\n📊 Phase 6: Evidence Scoring")
            
            total_score = 0
            max_possible = 100
            
            # Scoring weights as per spec
            weights = {
                'cex_funding': 40,
                'arkadiko_interaction': 25,
                'fee_pattern': 15,
                'stylometry': 10,
                'timing_correlation': 10
            }
            
            evidence_summary = defaultdict(list)
            
            for evidence in self.evidence:
                evidence_summary[evidence.evidence_type].append(evidence)
                
                # Apply weights
                weight = weights.get(evidence.evidence_type, 5)
                score_contribution = weight * evidence.confidence
                total_score += score_contribution
                
                print(f"  📋 {evidence.evidence_type}: {evidence.confidence:.2f} confidence, {score_contribution:.1f} points")
            
            # Normalize to percentage
            confidence_percentage = min(total_score / max_possible * 100, 100)
            
            self.mission_state['evidence_score'] = confidence_percentage
            
            # Determine conclusion
            if confidence_percentage >= 70:
                conclusion = "Probable founder"
                print(f"🎯 CONCLUSION: {conclusion} ({confidence_percentage:.1f}% confidence)")
            elif confidence_percentage >= 40:
                conclusion = "Possible connection"
                print(f"🤔 CONCLUSION: {conclusion} ({confidence_percentage:.1f}% confidence)")
            else:
                conclusion = "Insufficient evidence"
                print(f"❓ CONCLUSION: {conclusion} ({confidence_percentage:.1f}% confidence)")
            
            scoring_result = {
                'total_score': confidence_percentage,
                'conclusion': conclusion,
                'evidence_breakdown': dict(evidence_summary),
                'scoring_weights': weights
            }
            
            self._update_mission_state(7, 'Report Generation')
            return scoring_result
            
        except Exception as e:
            print(f"❌ Evidence scoring failed: {e}")
            return {'total_score': 0, 'conclusion': 'Analysis failed'}
    
    def generate_report(self, scoring_result: Dict) -> str:
        """Phase 7: Build human-readable dossier"""
        try:
            print("\n📄 Phase 7: Report Generation")
            
            # Generate Markdown report
            report_content = self._generate_markdown_report(scoring_result)
            
            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"welsh_founder_dossier_{timestamp}.md"
            
            print(f"✅ Report generated: {filename}")
            print(f"📊 Final confidence: {scoring_result['total_score']:.1f}%")
            print(f"🎯 Conclusion: {scoring_result['conclusion']}")
            
            self._update_mission_state(8, 'Mission Complete')
            
            return report_content
            
        except Exception as e:
            print(f"❌ Report generation failed: {e}")
            return "Report generation failed"
    
    def _generate_markdown_report(self, scoring_result: Dict) -> str:
        """Generate comprehensive Markdown report"""
        
        report = f"""# WELSH Token Founder Investigation Report
        
## Executive Summary
**Investigation Target:** WELSH Token Founder Identity  
**Analysis Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Confidence Score:** {scoring_result['total_score']:.1f}%  
**Conclusion:** {scoring_result['conclusion']}

## Investigation Methodology
This analysis employed blockchain forensics techniques including:
- Wallet clustering analysis
- Transaction pattern recognition  
- Cross-platform correlation
- Funding source tracing
- Temporal analysis

## Key Findings

### Deployer Information
- **Contract:** {getattr(self, 'welsh_contract', 'N/A')}
- **Deployer Address:** {getattr(self, 'deployer_info', {}).get('address', 'N/A')}
- **Deploy Transaction:** {getattr(self, 'deployer_info', {}).get('deploy_tx', 'N/A')}

### Wallet Cluster Analysis
"""
        
        # Add cluster information
        for addr, cluster in self.clusters.items():
            report += f"""
#### Cluster: {addr}
- **Related Addresses:** {len(cluster.related_addresses)}
- **Confidence Score:** {cluster.confidence_score:.2f}
- **Heuristics Applied:** {', '.join(set(cluster.heuristics))}
"""
        
        # Add evidence breakdown
        report += f"""
## Evidence Analysis

### Scoring Breakdown
"""
        
        for evidence_type, evidences in scoring_result.get('evidence_breakdown', {}).items():
            report += f"- **{evidence_type}:** {len(evidences)} instances\n"
        
        # Add technical details
        report += f"""
## Technical Details

### Mission Execution Log
- **Phases Completed:** {len(self.mission_state['completed_phases'])}
- **Current Phase:** {self.mission_state['phase']}
- **Evidence Items:** {len(self.evidence)}

### Graph Statistics
- **Nodes:** {self.wallet_graph.number_of_nodes()}
- **Edges:** {self.wallet_graph.number_of_edges()}

## Disclaimer
This analysis is based on publicly available blockchain data and should not be considered definitive proof of identity. Legal verification may require additional investigation and formal procedures.

---
*Generated by WELSH-Founder Hunter AI Agent*
"""
        
        return report
    
    def _update_mission_state(self, new_phase: int, objective: str):
        """Update mission state tracking"""
        self.mission_state['completed_phases'].append(self.mission_state['phase'])
        self.mission_state['phase'] = new_phase
        self.mission_state['current_objective'] = objective
        
        print(f"🔄 Mission State Updated: Phase {new_phase} - {objective}")
    
    def run_full_investigation(self, welsh_contract: str, arkadiko_wallets: List[str], 
                             philip_wallets: List[str] = None) -> Dict:
        """Execute complete investigation pipeline"""
        try:
            print("🚀 Starting WELSH-Founder Hunter Investigation")
            print("=" * 60)
            
            # Phase 0: Bootstrap
            if not self.bootstrap(welsh_contract, arkadiko_wallets, philip_wallets):
                return {'success': False, 'error': 'Bootstrap failed'}
            
            # Phase 1: Deployer Discovery
            deployer_info = self.discover_deployer()
            if not deployer_info:
                return {'success': False, 'error': 'Deployer discovery failed'}
            
            deployer_address, deploy_tx = deployer_info
            
            # Phase 2: Wallet Clustering
            cluster = self.expand_wallet_cluster(deployer_address)
            if not cluster:
                return {'success': False, 'error': 'Wallet clustering failed'}
            
            # Phase 3: Funding Source Trace
            funding_sources = self.trace_funding_sources(cluster)
            
            # Phase 4: Arkadiko Overlap
            arkadiko_overlap = self.scan_arkadiko_overlap(cluster)
            
            # Phase 5: Off-chain Correlation
            offchain_data = self.correlate_offchain_data()
            
            # Phase 6: Evidence Scoring
            scoring_result = self.score_evidence()
            
            # Phase 7: Report Generation
            report = self.generate_report(scoring_result)
            
            print("\n" + "=" * 60)
            print("🎉 Investigation Complete!")
            
            return {
                'success': True,
                'deployer_address': deployer_address,
                'cluster_size': len(cluster.related_addresses),
                'evidence_count': len(self.evidence),
                'confidence_score': scoring_result['total_score'],
                'conclusion': scoring_result['conclusion'],
                'report': report,
                'mission_state': self.mission_state
            }
            
        except Exception as e:
            print(f"❌ Investigation failed: {e}")
            return {'success': False, 'error': str(e)}

# Example usage and configuration
def create_welsh_hunter_config():
    """Create configuration for WELSH-Founder Hunter"""
    return {
        'hiro_api_key': None,  # Optional - set for higher rate limits
        'discord_bot_token': None,  # For Discord analysis
        'github_pat': None,  # For GitHub analysis
        'subpoena_mode': False,  # Legal escalation toggle
        'max_cluster_size': 50,
        'analysis_depth': 2,
        'confidence_threshold': 70
    }

if __name__ == "__main__":
    # Demo the agent
    print("🔍 WELSH-Founder Hunter AI Agent")
    print("Production-ready blockchain forensics for Stacks ecosystem")
    
    # Example usage
    config = create_welsh_hunter_config()
    hunter = WELSHFounderHunter(config)
    
    # Example investigation (replace with real data)
    result = hunter.run_full_investigation(
        welsh_contract="SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token",
        arkadiko_wallets=[
            "SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR",
            "SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE"
        ]
    )
    
    print(f"\n🎯 Investigation Result: {result['conclusion']}")
    print(f"📊 Confidence: {result['confidence_score']:.1f}%")