# Enhanced WELSH-Founder Hunter - Comprehensive Hiro API Utilization
# Utilizing every possible option for maximum blockchain forensics capability

import json
import requests
import networkx as nx
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import re
import statistics
import base58
from typing import Dict, List, Set, Tuple, Optional, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import time
from urllib.parse import urlencode

@dataclass
class TransactionPattern:
    """Advanced transaction pattern analysis"""
    address: str
    avg_fee: float
    fee_variance: float
    tx_frequency: float
    common_recipients: Set[str]
    time_patterns: List[int]  # Hour of day patterns
    amount_patterns: List[float]
    nonce_gaps: List[int]
    gas_efficiency: float
    batch_behavior: bool

@dataclass
class ContractInteraction:
    """Contract interaction analysis"""
    contract_address: str
    function_name: str
    caller: str
    timestamp: datetime
    tx_id: str
    success: bool
    events: List[Dict]
    gas_used: int
    contract_type: str

@dataclass
class AdvancedEvidence:
    """Enhanced evidence with correlation scores"""
    evidence_type: str
    description: str
    confidence: float
    correlation_score: float
    timestamp: datetime
    source_data: Dict
    supporting_evidence: List[str]
    risk_factors: List[str]
    blockchain_proof: Dict

@dataclass
class WalletCluster:
    """Enhanced wallet cluster with advanced metrics"""
    primary_address: str
    related_addresses: Set[str]
    confidence_score: float
    heuristics: List[str]
    first_seen: datetime
    last_seen: datetime
    cluster_type: str
    risk_score: float
    activity_correlation: float
    funding_sources: List[str]

class ComprehensiveHiroAPI:
    """Comprehensive Hiro API client utilizing all available endpoints"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.endpoints = {
            'mainnet': 'https://api.mainnet.hiro.so',
            'testnet': 'https://api.testnet.hiro.so',
            'backup_mainnet': 'https://stacks-node-api.mainnet.stacks.co',
            'backup_testnet': 'https://stacks-node-api.testnet.stacks.co'
        }
        
        self.current_endpoint = self.endpoints['mainnet']
        self.session = requests.Session()
        
        # Enhanced headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Enhanced-WELSH-Hunter/2.0',
            'Accept': 'application/json'
        }
        
        if api_key:
            headers['X-API-Key'] = api_key
            
        self.session.headers.update(headers)
        
        # Rate limiting
        self.rate_limit = {
            'requests_per_minute': 5000 if api_key else 500,
            'burst_limit': 100 if api_key else 20,
            'current_requests': 0,
            'minute_start': time.time(),
            'last_request': 0
        }
    
    def _rate_limit_check(self):
        """Intelligent rate limiting with burst support"""
        current_time = time.time()
        
        # Reset minute counter
        if current_time - self.rate_limit['minute_start'] > 60:
            self.rate_limit['current_requests'] = 0
            self.rate_limit['minute_start'] = current_time
        
        # Check burst limit
        time_since_last = current_time - self.rate_limit['last_request']
        if time_since_last < 0.1:  # 100ms minimum between requests
            time.sleep(0.1 - time_since_last)
        
        # Check minute limit
        if self.rate_limit['current_requests'] >= self.rate_limit['requests_per_minute']:
            sleep_time = 60 - (current_time - self.rate_limit['minute_start'])
            if sleep_time > 0:
                time.sleep(sleep_time)
                self.rate_limit['current_requests'] = 0
                self.rate_limit['minute_start'] = time.time()
        
        self.rate_limit['current_requests'] += 1
        self.rate_limit['last_request'] = time.time()
    
    def make_request(self, endpoint: str, params: Dict = None, retries: int = 3) -> Optional[Dict]:
        """Enhanced API request with comprehensive error handling"""
        self._rate_limit_check()
        
        for attempt in range(retries):
            try:
                url = f"{self.current_endpoint}{endpoint}"
                response = self.session.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    print(f"⚠️ Rate limited, attempt {attempt + 1}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                elif response.status_code == 404:
                    return None
                else:
                    print(f"⚠️ API error {response.status_code}: {endpoint}")
                    if attempt == retries - 1:
                        self._switch_endpoint()
                    continue
                    
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Request failed (attempt {attempt + 1}): {e}")
                if attempt == retries - 1:
                    self._switch_endpoint()
                time.sleep(1)
        
        return None
    
    def _switch_endpoint(self):
        """Switch to backup endpoint"""
        endpoints = list(self.endpoints.values())
        current_index = endpoints.index(self.current_endpoint)
        next_index = (current_index + 1) % len(endpoints)
        self.current_endpoint = endpoints[next_index]
        print(f"🔄 Switched to endpoint: {self.current_endpoint}")
    
    # Comprehensive API methods utilizing all Hiro endpoints
    
    def get_blockchain_status(self) -> Dict:
        """Get comprehensive blockchain status"""
        return self.make_request('/extended/v1/status') or {}
    
    def get_contract_info(self, contract_id: str) -> Dict:
        """Get detailed contract information"""
        return self.make_request(f'/extended/v1/contract/{contract_id}') or {}
    
    def get_contract_source(self, contract_id: str) -> Dict:
        """Get contract source code"""
        return self.make_request(f'/extended/v1/contract/{contract_id}/source') or {}
    
    def get_contract_interface(self, contract_id: str) -> Dict:
        """Get contract interface/ABI"""
        return self.make_request(f'/extended/v1/contract/{contract_id}/interface') or {}
    
    def get_contract_events(self, contract_id: str, limit: int = 100) -> Dict:
        """Get contract events"""
        params = {'limit': limit}
        return self.make_request(f'/extended/v1/contract/{contract_id}/events', params) or {}
    
    def get_transaction_details(self, tx_id: str) -> Dict:
        """Get comprehensive transaction details"""
        return self.make_request(f'/extended/v1/tx/{tx_id}') or {}
    
    def get_transaction_events(self, tx_id: str) -> Dict:
        """Get transaction events"""
        return self.make_request(f'/extended/v1/tx/{tx_id}/events') or {}
    
    def get_address_transactions(self, address: str, limit: int = 50, offset: int = 0) -> Dict:
        """Get address transaction history"""
        params = {'limit': limit, 'offset': offset}
        return self.make_request(f'/extended/v1/address/{address}/transactions', params) or {}
    
    def get_address_stx_balance(self, address: str) -> Dict:
        """Get STX balance and details"""
        return self.make_request(f'/extended/v1/address/{address}/stx') or {}
    
    def get_address_nonces(self, address: str) -> Dict:
        """Get address nonces"""
        return self.make_request(f'/extended/v1/address/{address}/nonces') or {}
    
    def get_address_assets(self, address: str) -> Dict:
        """Get all assets held by address"""
        return self.make_request(f'/extended/v1/address/{address}/assets') or {}
    
    def get_ft_holdings(self, address: str) -> Dict:
        """Get fungible token holdings"""
        return self.make_request(f'/extended/v1/tokens/ft/holdings/{address}') or {}
    
    def get_nft_holdings(self, address: str) -> Dict:
        """Get NFT holdings"""
        return self.make_request(f'/extended/v1/tokens/nft/holdings/{address}') or {}
    
    def get_mempool_transactions(self, address: str = None) -> Dict:
        """Get mempool transactions"""
        params = {}
        if address:
            params['sender_address'] = address
        return self.make_request('/extended/v1/tx/mempool', params) or {}
    
    def get_block_info(self, block_hash_or_height: Union[str, int]) -> Dict:
        """Get block information"""
        return self.make_request(f'/extended/v1/block/{block_hash_or_height}') or {}
    
    def get_block_transactions(self, block_hash_or_height: Union[str, int]) -> Dict:
        """Get transactions in a block"""
        return self.make_request(f'/extended/v1/block/{block_hash_or_height}/transactions') or {}
    
    def search_transactions(self, **kwargs) -> Dict:
        """Search transactions with filters"""
        return self.make_request('/extended/v1/tx', kwargs) or {}
    
    def get_fee_rate(self) -> Dict:
        """Get current fee rates"""
        return self.make_request('/extended/v1/fee_rate') or {}
    
    def get_network_info(self) -> Dict:
        """Get network information"""
        return self.make_request('/v2/info') or {}
    
    def get_pox_info(self) -> Dict:
        """Get Proof of Transfer information"""
        return self.make_request('/v2/pox') or {}

class EnhancedWELSHFounderHunter:
    """
    Enhanced WELSH-Founder Hunter utilizing comprehensive Hiro API capabilities
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.api = ComprehensiveHiroAPI(config.get('hiro_api_key'))
        
        # Enhanced data stores
        self.wallet_graph = nx.DiGraph()
        self.clusters = {}
        self.evidence = []
        self.transaction_patterns = {}
        self.contract_interactions = []
        self.address_metadata = {}
        self.blockchain_state = {}
        
        # Comprehensive service identification database
        self.service_database = self._load_comprehensive_services()
        
        # Advanced heuristics configuration
        self.heuristics_config = {
            'temporal_correlation_window': 3600,  # 1 hour
            'amount_similarity_threshold': 0.95,
            'fee_pattern_threshold': 0.9,
            'timing_pattern_threshold': 0.8,
            'nonce_gap_significance': 5,
            'cluster_confidence_minimum': 0.3,
            'evidence_correlation_minimum': 0.5
        }
        
        # Mission state with comprehensive tracking
        self.mission_state = {
            'phase': 0,
            'completed_phases': [],
            'current_objective': 'Comprehensive Bootstrap',
            'evidence_score': 0,
            'api_calls_made': 0,
            'addresses_analyzed': 0,
            'patterns_detected': 0,
            'contracts_analyzed': 0,
            'blocks_examined': 0,
            'total_transactions_processed': 0
        }
        
        print("🔍 Enhanced WELSH-Founder Hunter initialized")
        print(f"🌐 API endpoint: {self.api.current_endpoint}")
        print(f"⚡ Rate limit: {self.api.rate_limit['requests_per_minute']} req/min")
        print(f"📊 Mission State: Phase {self.mission_state['phase']} - {self.mission_state['current_objective']}")
    
    def _load_comprehensive_services(self) -> Dict[str, Dict]:
        """Load comprehensive service identification database"""
        return {
            # Major CEX addresses (these would be real addresses in production)
            'SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE': {
                'service': 'binance', 'type': 'hot_wallet', 'confidence': 0.95,
                'risk_level': 'low', 'kyc_required': True
            },
            'SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7': {
                'service': 'binance', 'type': 'hot_wallet_2', 'confidence': 0.95,
                'risk_level': 'low', 'kyc_required': True
            },
            'SP1Y5YSTAHZ88XYK1VPDH24GY0HPX5J4JECTMY4A1': {
                'service': 'okx', 'type': 'hot_wallet', 'confidence': 0.90,
                'risk_level': 'low', 'kyc_required': True
            },
            'SP32AEEF6WW5Y0NMJ1S8SBSZDAY8R5J32NBZFPKKZ': {
                'service': 'kucoin', 'type': 'hot_wallet', 'confidence': 0.90,
                'risk_level': 'medium', 'kyc_required': True
            },
            
            # DeFi protocols
            'SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR': {
                'service': 'arkadiko', 'type': 'protocol', 'confidence': 1.0,
                'risk_level': 'low', 'decentralized': True
            },
            'SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9': {
                'service': 'alex', 'type': 'dex', 'confidence': 0.95,
                'risk_level': 'low', 'decentralized': True
            },
            
            # Stacking pools
            'SP1GPBP8NBRXDRJBFQBV7KMAZX1Z8QJ5QWMSS1M1': {
                'service': 'stacking_pool', 'type': 'delegation', 'confidence': 0.85,
                'risk_level': 'medium', 'stacking_related': True
            },
            
            # Known ecosystem addresses
            'SP000000000000000000002Q6VF78': {
                'service': 'stacks_foundation', 'type': 'genesis', 'confidence': 1.0,
                'risk_level': 'none', 'official': True
            }
        }
    
    def comprehensive_bootstrap(self, welsh_contract: str, arkadiko_wallets: List[str], 
                               philip_wallets: List[str] = None) -> bool:
        """Comprehensive Phase 0: Bootstrap with full blockchain state analysis"""
        try:
            print("\n🚀 Comprehensive Phase 0: Bootstrap")
            
            # Validate inputs
            if not self._validate_stacks_address(welsh_contract):
                print(f"❌ Invalid WELSH contract address: {welsh_contract}")
                return False
            
            for addr in arkadiko_wallets:
                if not self._validate_stacks_address(addr):
                    print(f"❌ Invalid Arkadiko address: {addr}")
                    return False
            
            # Store validated data
            self.welsh_contract = welsh_contract
            self.arkadiko_wallets = set(arkadiko_wallets)
            self.philip_wallets = set(philip_wallets or [])
            
            # Get comprehensive blockchain state
            print("📊 Gathering blockchain state...")
            self.blockchain_state = {
                'status': self.api.get_blockchain_status(),
                'network_info': self.api.get_network_info(),
                'pox_info': self.api.get_pox_info(),
                'fee_rates': self.api.get_fee_rate(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Validate blockchain connection
            if not self.blockchain_state['status']:
                print("❌ Failed to connect to blockchain")
                return False
            
            # Pre-populate service database with known addresses
            for addr in self.arkadiko_wallets:
                if addr not in self.service_database:
                    self.service_database[addr] = {
                        'service': 'arkadiko_ops', 'type': 'operational', 
                        'confidence': 0.8, 'risk_level': 'low'
                    }
            
            # Get initial contract information
            print("🔍 Analyzing WELSH contract...")
            welsh_info = self.api.get_contract_info(welsh_contract)
            if welsh_info:
                print(f"✅ WELSH contract validated")
                print(f"   Deploy block: {welsh_info.get('block_height', 'Unknown')}")
                print(f"   Source code: {len(welsh_info.get('source_code', ''))} chars")
            
            # Display comprehensive status
            chain_tip = self.blockchain_state['status'].get('chain_tip', {})
            print(f"✅ Connected to Stacks blockchain")
            print(f"   Chain tip: Block {chain_tip.get('block_height', 'Unknown')}")
            print(f"   Network: {self.blockchain_state['status'].get('network_id', 'Unknown')}")
            print(f"   Burn block: {chain_tip.get('burn_block_height', 'Unknown')}")
            
            print(f"✅ Loaded WELSH contract: {welsh_contract}")
            print(f"✅ Loaded {len(self.arkadiko_wallets)} Arkadiko wallets")
            print(f"✅ Loaded {len(self.philip_wallets)} Philip wallets")
            print(f"✅ Service database: {len(self.service_database)} known addresses")
            
            self._update_mission_state(1, 'Comprehensive Deployer Discovery')
            return True
            
        except Exception as e:
            print(f"❌ Comprehensive bootstrap failed: {e}")
            return False
    
    def _validate_stacks_address(self, address: str) -> bool:
        """Validate Stacks address format"""
        if not address or len(address) != 41:
            return False
        if not address.startswith(('SP', 'SM')):
            return False
        
        # Basic character validation
        valid_chars = set('0123456789ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz')
        return all(c in valid_chars for c in address[2:])
    
    def comprehensive_deployer_discovery(self) -> Optional[Tuple[str, str, Dict]]:
        """Comprehensive Phase 1: Advanced deployer discovery with full analysis"""
        try:
            print("\n🔍 Comprehensive Phase 1: Deployer Discovery")
            
            # Get comprehensive contract information
            contract_info = self.api.get_contract_info(self.welsh_contract)
            if not contract_info:
                print("❌ Failed to fetch contract information")
                return None
            
            # Get contract source and interface
            contract_source = self.api.get_contract_source(self.welsh_contract)
            contract_interface = self.api.get_contract_interface(self.welsh_contract)
            
            deploy_tx = contract_info.get('tx_id')
            source_code = contract_info.get('source_code', '')
            
            print(f"✅ Contract analysis complete")
            print(f"   Deploy TX: {deploy_tx}")
            print(f"   Source code: {len(source_code)} characters")
            print(f"   Functions: {len(contract_interface.get('functions', []))}")
            
            # Get comprehensive transaction details
            tx_details = self.api.get_transaction_details(deploy_tx)
            tx_events = self.api.get_transaction_events(deploy_tx)
            
            if not tx_details:
                print("❌ Failed to fetch deployment transaction")
                return None
            
            deployer = tx_details.get('sender_address')
            deploy_time = tx_details.get('burn_block_time_iso')
            block_height = tx_details.get('block_height')
            
            # Get deployer's comprehensive data
            print(f"📊 Analyzing deployer: {deployer}")
            deployer_data = self._get_comprehensive_address_analysis(deployer)
            
            # Get deployment block context
            block_info = self.api.get_block_info(block_height) if block_height else {}
            block_transactions = self.api.get_block_transactions(block_height) if block_height else {}
            
            # Advanced deployment analysis
            deployment_analysis = self._analyze_deployment_context(
                tx_details, tx_events, deployer_data, block_info, block_transactions
            )
            
            # Comprehensive deployer profile
            self.deployer_info = {
                'address': deployer,
                'deploy_tx': deploy_tx,
                'deploy_time': deploy_time,
                'block_height': block_height,
                'fee_rate': tx_details.get('fee_rate', 0),
                'nonce': tx_details.get('nonce', 0),
                'tx_status': tx_details.get('tx_status'),
                'source_code_hash': hashlib.sha256(source_code.encode()).hexdigest(),
                'contract_complexity': len(contract_interface.get('functions', [])),
                'deployment_analysis': deployment_analysis,
                'deployer_profile': deployer_data,
                'block_context': {
                    'block_transactions': len(block_transactions.get('results', [])),
                    'block_time': block_info.get('burn_block_time_iso'),
                    'concurrent_deployments': self._count_concurrent_deployments(block_transactions)
                }
            }
            
            print(f"✅ Comprehensive deployer analysis complete")
            print(f"   Deployer: {deployer}")
            print(f"   Risk score: {deployment_analysis.get('risk_score', 0):.2f}")
            print(f"   Activity level: {deployer_data.get('activity_level', 'unknown')}")
            print(f"   Service classification: {deployer_data.get('service_classification', 'unknown')}")
            
            self._update_mission_state(2, 'Advanced Wallet Clustering')
            return deployer, deploy_tx, self.deployer_info
            
        except Exception as e:
            print(f"❌ Comprehensive deployer discovery failed: {e}")
            return None
    
    def _get_comprehensive_address_analysis(self, address: str) -> Dict:
        """Get comprehensive address analysis using all available API endpoints"""
        try:
            print(f"  📊 Comprehensive analysis for {address}")
            
            # Get all available data
            stx_balance = self.api.get_address_stx_balance(address)
            nonces = self.api.get_address_nonces(address)
            assets = self.api.get_address_assets(address)
            ft_holdings = self.api.get_ft_holdings(address)
            nft_holdings = self.api.get_nft_holdings(address)
            
            # Get transaction history in batches
            all_transactions = []
            offset = 0
            batch_size = 50
            
            while len(all_transactions) < 500:  # Limit to prevent excessive API calls
                tx_batch = self.api.get_address_transactions(address, batch_size, offset)
                if not tx_batch or not tx_batch.get('results'):
                    break
                
                all_transactions.extend(tx_batch['results'])
                
                if len(tx_batch['results']) < batch_size:
                    break
                    
                offset += batch_size
                self.mission_state['api_calls_made'] += 1
            
            # Advanced pattern analysis
            patterns = self._analyze_advanced_patterns(all_transactions)
            
            # Activity classification
            activity_level = self._classify_activity_level(all_transactions, patterns)
            
            # Service classification
            service_classification = self._classify_service_type(address, all_transactions, patterns)
            
            # Risk assessment
            risk_assessment = self._assess_address_risk(address, all_transactions, patterns)
            
            # Temporal analysis
            temporal_analysis = self._analyze_temporal_patterns(all_transactions)
            
            comprehensive_data = {
                'address': address,
                'stx_balance': stx_balance.get('balance', 0) if stx_balance else 0,
                'locked_stx': stx_balance.get('locked', 0) if stx_balance else 0,
                'nonces': nonces,
                'total_transactions': len(all_transactions),
                'ft_holdings': ft_holdings.get('results', []) if ft_holdings else [],
                'nft_holdings': nft_holdings.get('results', []) if nft_holdings else [],
                'patterns': patterns,
                'activity_level': activity_level,
                'service_classification': service_classification,
                'risk_assessment': risk_assessment,
                'temporal_analysis': temporal_analysis,
                'first_seen': min([tx.get('burn_block_time_iso') for tx in all_transactions if tx.get('burn_block_time_iso')], default=None),
                'last_seen': max([tx.get('burn_block_time_iso') for tx in all_transactions if tx.get('burn_block_time_iso')], default=None),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            # Cache the analysis
            self.address_metadata[address] = comprehensive_data
            self.mission_state['addresses_analyzed'] += 1
            self.mission_state['total_transactions_processed'] += len(all_transactions)
            
            return comprehensive_data
            
        except Exception as e:
            print(f"⚠️ Comprehensive address analysis failed for {address}: {e}")
            return {'address': address, 'error': str(e)}
    
    def _analyze_advanced_patterns(self, transactions: List[Dict]) -> Dict:
        """Advanced transaction pattern analysis"""
        try:
            if not transactions:
                return {}
            
            # Fee analysis
            fees = [tx.get('fee_rate', 0) for tx in transactions if tx.get('fee_rate')]
            fee_analysis = {
                'avg_fee': statistics.mean(fees) if fees else 0,
                'median_fee': statistics.median(fees) if fees else 0,
                'fee_variance': statistics.variance(fees) if len(fees) > 1 else 0,
                'fee_consistency': len(set(fees)) / len(fees) if fees else 0
            }
            
            # Timing analysis
            timestamps = [tx.get('burn_block_time') for tx in transactions if tx.get('burn_block_time')]
            timing_analysis = {}
            
            if timestamps:
                # Time gaps between transactions
                sorted_times = sorted(timestamps)
                gaps = [sorted_times[i] - sorted_times[i-1] for i in range(1, len(sorted_times))]
                
                timing_analysis = {
                    'avg_gap_seconds': statistics.mean(gaps) if gaps else 0,
                    'median_gap_seconds': statistics.median(gaps) if gaps else 0,
                    'regular_intervals': self._detect_regular_intervals(gaps),
                    'burst_activity': self._detect_burst_activity(timestamps),
                    'time_of_day_patterns': self._analyze_time_patterns(timestamps)
                }
            
            # Amount analysis
            amounts = []
            for tx in transactions:
                if tx.get('tx_type') == 'token_transfer':
                    amount = tx.get('token_transfer', {}).get('amount', 0)
                    if amount:
                        amounts.append(amount)
            
            amount_analysis = {}
            if amounts:
                amount_analysis = {
                    'avg_amount': statistics.mean(amounts),
                    'median_amount': statistics.median(amounts),
                    'round_number_frequency': sum(1 for a in amounts if a % 1000000 == 0) / len(amounts),
                    'amount_diversity': len(set(amounts)) / len(amounts),
                    'large_transactions': sum(1 for a in amounts if a > statistics.mean(amounts) * 10)
                }
            
            # Nonce analysis
            nonces = [tx.get('nonce') for tx in transactions if tx.get('nonce') is not None]
            nonce_analysis = {}
            
            if nonces:
                sorted_nonces = sorted(nonces)
                gaps = [sorted_nonces[i] - sorted_nonces[i-1] for i in range(1, len(sorted_nonces))]
                
                nonce_analysis = {
                    'sequential_ratio': sum(1 for g in gaps if g == 1) / len(gaps) if gaps else 0,
                    'large_gaps': sum(1 for g in gaps if g > 10) if gaps else 0,
                    'gap_pattern': 'sequential' if all(g == 1 for g in gaps[:10]) else 'irregular'
                }
            
            # Counterparty analysis
            counterparties = set()
            for tx in transactions:
                sender = tx.get('sender_address')
                if sender:
                    counterparties.add(sender)
                
                if tx.get('tx_type') == 'token_transfer':
                    recipient = tx.get('token_transfer', {}).get('recipient_address')
                    if recipient:
                        counterparties.add(recipient)
            
            counterparty_analysis = {
                'unique_counterparties': len(counterparties),
                'counterparty_diversity': len(counterparties) / len(transactions) if transactions else 0,
                'repeat_interactions': len(transactions) - len(counterparties)
            }
            
            return {
                'fee_analysis': fee_analysis,
                'timing_analysis': timing_analysis,
                'amount_analysis': amount_analysis,
                'nonce_analysis': nonce_analysis,
                'counterparty_analysis': counterparty_analysis,
                'pattern_confidence': self._calculate_pattern_confidence(fee_analysis, timing_analysis, amount_analysis)
            }
            
        except Exception as e:
            print(f"⚠️ Advanced pattern analysis failed: {e}")
            return {}
    
    def _detect_regular_intervals(self, gaps: List[int]) -> bool:
        """Detect if transactions occur at regular intervals"""
        if len(gaps) < 5:
            return False
        
        # Check if gaps are similar (within 20% variance)
        avg_gap = statistics.mean(gaps)
        variance = statistics.variance(gaps)
        coefficient_of_variation = (variance ** 0.5) / avg_gap if avg_gap > 0 else float('inf')
        
        return coefficient_of_variation < 0.2
    
    def _detect_burst_activity(self, timestamps: List[int]) -> Dict:
        """Detect burst activity patterns"""
        if len(timestamps) < 10:
            return {'detected': False}
        
        # Sort timestamps
        sorted_times = sorted(timestamps)
        
        # Find clusters of activity (transactions within 1 hour)
        clusters = []
        current_cluster = [sorted_times[0]]
        
        for i in range(1, len(sorted_times)):
            if sorted_times[i] - sorted_times[i-1] <= 3600:  # 1 hour
                current_cluster.append(sorted_times[i])
            else:
                if len(current_cluster) >= 5:  # Burst = 5+ transactions in 1 hour
                    clusters.append(current_cluster)
                current_cluster = [sorted_times[i]]
        
        if len(current_cluster) >= 5:
            clusters.append(current_cluster)
        
        return {
            'detected': len(clusters) > 0,
            'burst_count': len(clusters),
            'largest_burst': max(len(cluster) for cluster in clusters) if clusters else 0,
            'burst_frequency': len(clusters) / (len(sorted_times) / 100) if sorted_times else 0
        }
    
    def _analyze_time_patterns(self, timestamps: List[int]) -> Dict:
        """Analyze time-of-day patterns"""
        if not timestamps:
            return {}
        
        hours = []
        days_of_week = []
        
        for ts in timestamps:
            try:
                dt = datetime.fromtimestamp(ts)
                hours.append(dt.hour)
                days_of_week.append(dt.weekday())
            except:
                continue
        
        if not hours:
            return {}
        
        # Analyze hour distribution
        hour_counts = Counter(hours)
        peak_hours = [hour for hour, count in hour_counts.most_common(3)]
        
        # Analyze day distribution
        day_counts = Counter(days_of_week)
        
        return {
            'peak_hours': peak_hours,
            'hour_distribution': dict(hour_counts),
            'day_distribution': dict(day_counts),
            'business_hours_ratio': sum(hour_counts[h] for h in range(9, 17)) / len(hours),
            'weekend_ratio': sum(day_counts[d] for d in [5, 6]) / len(days_of_week) if days_of_week else 0
        }
    
    def _calculate_pattern_confidence(self, fee_analysis: Dict, timing_analysis: Dict, amount_analysis: Dict) -> float:
        """Calculate overall pattern confidence score"""
        confidence = 0.0
        
        # Fee consistency contributes to confidence
        if fee_analysis.get('fee_consistency', 0) > 0.8:
            confidence += 0.3
        
        # Regular timing patterns
        if timing_analysis.get('regular_intervals', False):
            confidence += 0.3
        
        # Amount patterns
        if amount_analysis.get('round_number_frequency', 0) > 0.5:
            confidence += 0.2
        
        # Burst activity indicates automation
        if timing_analysis.get('burst_activity', {}).get('detected', False):
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _classify_activity_level(self, transactions: List[Dict], patterns: Dict) -> str:
        """Classify address activity level"""
        tx_count = len(transactions)
        
        if tx_count == 0:
            return 'inactive'
        elif tx_count < 10:
            return 'low'
        elif tx_count < 100:
            return 'medium'
        elif tx_count < 1000:
            return 'high'
        else:
            return 'very_high'
    
    def _classify_service_type(self, address: str, transactions: List[Dict], patterns: Dict) -> str:
        """Classify the type of service this address represents"""
        # Check known services first
        if address in self.service_database:
            return self.service_database[address]['service']
        
        # Analyze patterns to classify
        tx_count = len(transactions)
        
        # High volume + regular patterns = likely exchange
        if (tx_count > 1000 and 
            patterns.get('timing_analysis', {}).get('regular_intervals', False)):
            return 'exchange_suspected'
        
        # Burst activity + round amounts = likely automated service
        if (patterns.get('timing_analysis', {}).get('burst_activity', {}).get('detected', False) and
            patterns.get('amount_analysis', {}).get('round_number_frequency', 0) > 0.7):
            return 'automated_service'
        
        # Low activity + irregular patterns = likely individual
        if tx_count < 50:
            return 'individual_suspected'
        
        return 'unknown'
    
    def _assess_address_risk(self, address: str, transactions: List[Dict], patterns: Dict) -> Dict:
        """Assess risk factors for an address"""
        risk_factors = []
        risk_score = 0.0
        
        # High transaction volume
        if len(transactions) > 10000:
            risk_factors.append('very_high_volume')
            risk_score += 0.3
        
        # Unusual timing patterns
        burst_activity = patterns.get('timing_analysis', {}).get('burst_activity', {})
        if burst_activity.get('detected', False) and burst_activity.get('burst_count', 0) > 10:
            risk_factors.append('suspicious_burst_activity')
            risk_score += 0.4
        
        # Round number transactions (possible money laundering)
        round_freq = patterns.get('amount_analysis', {}).get('round_number_frequency', 0)
        if round_freq > 0.8:
            risk_factors.append('excessive_round_amounts')
            risk_score += 0.3
        
        # Inconsistent fee patterns
        fee_variance = patterns.get('fee_analysis', {}).get('fee_variance', 0)
        if fee_variance > 1000000:  # High fee variance
            risk_factors.append('inconsistent_fees')
            risk_score += 0.2
        
        # Known high-risk service
        service_info = self.service_database.get(address, {})
        if service_info.get('risk_level') == 'high':
            risk_factors.append('high_risk_service')
            risk_score += 0.5
        
        return {
            'risk_score': min(risk_score, 1.0),
            'risk_factors': risk_factors,
            'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.3 else 'low'
        }
    
    def _analyze_temporal_patterns(self, transactions: List[Dict]) -> Dict:
        """Analyze temporal patterns in transactions"""
        if not transactions:
            return {}
        
        # Extract timestamps
        timestamps = [tx.get('burn_block_time') for tx in transactions if tx.get('burn_block_time')]
        
        if len(timestamps) < 2:
            return {}
        
        # Sort timestamps
        sorted_times = sorted(timestamps)
        
        # Calculate activity periods
        first_tx = datetime.fromtimestamp(sorted_times[0])
        last_tx = datetime.fromtimestamp(sorted_times[-1])
        total_period = (last_tx - first_tx).total_seconds()
        
        # Find active periods (periods with transactions)
        active_periods = []
        current_period_start = sorted_times[0]
        
        for i in range(1, len(sorted_times)):
            gap = sorted_times[i] - sorted_times[i-1]
            if gap > 86400:  # 24 hours gap = new period
                active_periods.append((current_period_start, sorted_times[i-1]))
                current_period_start = sorted_times[i]
        
        active_periods.append((current_period_start, sorted_times[-1]))
        
        return {
            'total_period_days': total_period / 86400,
            'active_periods': len(active_periods),
            'longest_inactive_period': max([active_periods[i][0] - active_periods[i-1][1] 
                                          for i in range(1, len(active_periods))], default=0) / 86400,
            'activity_consistency': len(active_periods) / (total_period / 86400) if total_period > 0 else 0
        }
    
    def _analyze_deployment_context(self, tx_details: Dict, tx_events: Dict, 
                                   deployer_data: Dict, block_info: Dict, 
                                   block_transactions: Dict) -> Dict:
        """Analyze deployment context for suspicious patterns"""
        try:
            analysis = {
                'risk_score': 0.0,
                'risk_factors': [],
                'deployment_timing': 'normal',
                'block_context': 'normal',
                'deployer_profile': 'normal'
            }
            
            # Analyze deployment timing
            deploy_time = tx_details.get('burn_block_time')
            if deploy_time:
                dt = datetime.fromtimestamp(deploy_time)
                hour = dt.hour
                
                # Suspicious timing
                if hour < 6 or hour > 22:
                    analysis['risk_factors'].append('unusual_deployment_time')
                    analysis['deployment_timing'] = 'suspicious'
                    analysis['risk_score'] += 0.2
            
            # Analyze block context
            block_tx_count = len(block_transactions.get('results', []))
            if block_tx_count > 100:  # Very busy block
                analysis['risk_factors'].append('deployed_in_busy_block')
                analysis['block_context'] = 'suspicious'
                analysis['risk_score'] += 0.1
            
            # Analyze deployer profile
            deployer_risk = deployer_data.get('risk_assessment', {}).get('risk_score', 0)
            if deployer_risk > 0.7:
                analysis['risk_factors'].append('high_risk_deployer')
                analysis['deployer_profile'] = 'high_risk'
                analysis['risk_score'] += 0.4
            
            # Check for preparation patterns
            deployer_activity = deployer_data.get('activity_level', 'unknown')
            if deployer_activity == 'very_high':
                analysis['risk_factors'].append('very_active_deployer')
                analysis['risk_score'] += 0.2
            
            return analysis
            
        except Exception as e:
            print(f"⚠️ Deployment context analysis failed: {e}")
            return {'risk_score': 0.0, 'error': str(e)}
    
    def _count_concurrent_deployments(self, block_transactions: Dict) -> int:
        """Count concurrent contract deployments in the same block"""
        if not block_transactions or 'results' not in block_transactions:
            return 0
        
        deployment_count = 0
        for tx in block_transactions['results']:
            if tx.get('tx_type') == 'smart_contract':
                deployment_count += 1
        
        return deployment_count
    
    def _update_mission_state(self, new_phase: int, objective: str):
        """Update mission state with comprehensive tracking"""
        self.mission_state['completed_phases'].append(self.mission_state['phase'])
        self.mission_state['phase'] = new_phase
        self.mission_state['current_objective'] = objective
        
        print(f"🔄 Mission State Updated: Phase {new_phase} - {objective}")
        print(f"   📊 API calls: {self.mission_state['api_calls_made']}")
        print(f"   🔍 Addresses analyzed: {self.mission_state['addresses_analyzed']}")
        print(f"   📈 Transactions processed: {self.mission_state['total_transactions_processed']}")
    
    def run_comprehensive_investigation(self, welsh_contract: str, arkadiko_wallets: List[str], 
                                       philip_wallets: List[str] = None) -> Dict:
        """Run comprehensive investigation utilizing all Hiro API capabilities"""
        try:
            print("🚀 Starting Comprehensive WELSH-Founder Hunter Investigation")
            print("=" * 70)
            
            # Phase 0: Comprehensive Bootstrap
            if not self.comprehensive_bootstrap(welsh_contract, arkadiko_wallets, philip_wallets):
                return {'success': False, 'error': 'Comprehensive bootstrap failed'}
            
            # Phase 1: Comprehensive Deployer Discovery
            deployer_info = self.comprehensive_deployer_discovery()
            if not deployer_info:
                return {'success': False, 'error': 'Comprehensive deployer discovery failed'}
            
            deployer_address, deploy_tx, deployer_data = deployer_info
            
            print("\n" + "=" * 70)
            print("🎉 Comprehensive Investigation Complete!")
            print(f"📊 Total API calls made: {self.mission_state['api_calls_made']}")
            print(f"🔍 Addresses analyzed: {self.mission_state['addresses_analyzed']}")
            print(f"📈 Transactions processed: {self.mission_state['total_transactions_processed']}")
            
            return {
                'success': True,
                'deployer_address': deployer_address,
                'deployer_risk_score': deployer_data['deployment_analysis']['risk_score'],
                'deployer_activity_level': deployer_data['deployer_profile']['activity_level'],
                'api_calls_made': self.mission_state['api_calls_made'],
                'addresses_analyzed': self.mission_state['addresses_analyzed'],
                'comprehensive_data': deployer_data,
                'mission_state': self.mission_state
            }
            
        except Exception as e:
            print(f"❌ Comprehensive investigation failed: {e}")
            return {'success': False, 'error': str(e)}

# Demo the comprehensive enhanced agent
if __name__ == "__main__":
    print("🔍 Enhanced WELSH-Founder Hunter - Comprehensive Hiro API Utilization")
    print("=" * 70)
    
    # Enhanced configuration
    config = {
        'hiro_api_key': None,  # Set your API key for full capabilities
        'max_cluster_size': 200,
        'analysis_depth': 5,
        'confidence_threshold': 80,
        'enable_advanced_heuristics': True,
        'comprehensive_analysis': True,
        'deep_pattern_analysis': True,
        'legal_review_required': False
    }
    
    print("✅ Enhanced configuration loaded")
    print("🚀 Initializing comprehensive hunter...")
    
    hunter = EnhancedWELSHFounderHunter(config)
    
    print(f"\n🎯 Ready for comprehensive investigation!")
    print(f"📊 Utilizing {len(hunter.api.endpoints)} API endpoints")
    print(f"🔍 Service database: {len(hunter.service_database)} known addresses")
    print(f"⚡ Rate limit: {hunter.api.rate_limit['requests_per_minute']} requests/minute")
    
    # Example usage
    print(f"\n📋 Example usage:")
    print(f"result = hunter.run_comprehensive_investigation(")
    print(f"    welsh_contract='SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token',")
    print(f"    arkadiko_wallets=['SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR']")
    print(f")")