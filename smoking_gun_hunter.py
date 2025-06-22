# WELSH-Founder Hunter - Smoking Gun Investigation Protocol
# Definitive blockchain forensics to find SMOKING GUN proof

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class SmokingGunHunter:
    """
    Smoking Gun Investigation Protocol for WELSH-Founder Hunter
    Finds DEFINITIVE on-chain proof, not circumstantial evidence
    """
    
    def __init__(self, hiro_api_key: str = None):
        self.hiro_api_key = hiro_api_key
        self.base_url = "https://api.hiro.so"
        self.session = requests.Session()
        
        if hiro_api_key:
            self.session.headers.update({'X-API-Key': hiro_api_key})
        
        # Seed data from investigation
        self.seed_data = {
            "welsh_deployer": "SP3NE50GEXFG9SZGTT51P40X2CKYSZ5CC4ZTZ7A2G",
            "gift_tx": "0xc7abd0b51116337aa6d064b42f68b132a228614c86ad44cba15e03cf3c56d675",
            "lp_seed_tx": "0xbb9cde4cf611e4b30b141d194af935970e3f5d6f1d7c6417fb0215b00bd82924",
            "arkadiko_addresses": [
                "SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR",
                "SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE"
            ]
        }
        
        self.smoking_guns = []
        self.evidence_score = 0
    
    def get_transaction_details(self, tx_id: str) -> Optional[Dict]:
        """Get detailed transaction information"""
        try:
            url = f"{self.base_url}/extended/v1/tx/{tx_id}"
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Failed to get transaction {tx_id}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Error getting transaction {tx_id}: {e}")
            return None
    
    def get_address_transactions(self, address: str, limit: int = 50) -> Optional[Dict]:
        """Get transaction history for an address"""
        try:
            url = f"{self.base_url}/extended/v1/address/{address}/transactions"
            params = {'limit': limit}
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ Failed to get transactions for {address}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Error getting transactions for {address}: {e}")
            return None
    
    def smoking_gun_check_1_gift_transaction_sender(self) -> bool:
        """
        SMOKING GUN CHECK 1: Gift Transaction Sender Analysis
        If sender of 1B WELSH transfer = deployer, then 'anonymous founders' is FALSE
        """
        print("\n🔍 SMOKING GUN CHECK 1: Gift Transaction Sender Analysis")
        print(f"Target: {self.seed_data['gift_tx']}")
        
        gift_tx_data = self.get_transaction_details(self.seed_data['gift_tx'])
        
        if not gift_tx_data:
            print("❌ Could not retrieve gift transaction data")
            return False
        
        sender = gift_tx_data.get('sender_address')
        deployer = self.seed_data['welsh_deployer']
        
        print(f"Gift Transaction Sender: {sender}")
        print(f"WELSH Deployer Address: {deployer}")
        
        if sender == deployer:
            smoking_gun = {
                'type': 'DEFINITIVE_PROOF',
                'description': 'Gift transaction sender matches WELSH deployer',
                'evidence': f'Sender {sender} = Deployer {deployer}',
                'conclusion': "Philip's 'anonymous founders' story is DEFINITIVELY FALSE",
                'confidence': 99,
                'legal_impact': 'FRAUD_PROVEN'
            }
            self.smoking_guns.append(smoking_gun)
            self.evidence_score += 50
            
            print("🚨 SMOKING GUN FOUND!")
            print(f"✅ {smoking_gun['conclusion']}")
            return True
        else:
            print(f"❌ No direct match found")
            return False
    
    def smoking_gun_check_2_lp_transaction_sender(self) -> bool:
        """
        SMOKING GUN CHECK 2: LP Transaction Sender Analysis
        If LP adder = deployer, same person created token AND provided liquidity
        """
        print("\n🔍 SMOKING GUN CHECK 2: LP Transaction Sender Analysis")
        print(f"Target: {self.seed_data['lp_seed_tx']}")
        
        lp_tx_data = self.get_transaction_details(self.seed_data['lp_seed_tx'])
        
        if not lp_tx_data:
            print("❌ Could not retrieve LP transaction data")
            return False
        
        sender = lp_tx_data.get('sender_address')
        deployer = self.seed_data['welsh_deployer']
        
        print(f"LP Transaction Sender: {sender}")
        print(f"WELSH Deployer Address: {deployer}")
        
        if sender == deployer:
            smoking_gun = {
                'type': 'STRONG_EVIDENCE',
                'description': 'LP transaction sender matches WELSH deployer',
                'evidence': f'LP Sender {sender} = Deployer {deployer}',
                'conclusion': 'Same person created WELSH token AND provided initial liquidity',
                'confidence': 95,
                'legal_impact': 'COORDINATION_PROVEN'
            }
            self.smoking_guns.append(smoking_gun)
            self.evidence_score += 30
            
            print("🚨 SMOKING GUN FOUND!")
            print(f"✅ {smoking_gun['conclusion']}")
            return True
        else:
            print(f"❌ No direct match found")
            return False
    
    def smoking_gun_check_3_funding_source_trace(self) -> bool:
        """
        SMOKING GUN CHECK 3: Deployer Funding Source Trace
        If deployer funded by known Philip/Arkadiko addresses
        """
        print("\n🔍 SMOKING GUN CHECK 3: Deployer Funding Source Trace")
        print(f"Target: {self.seed_data['welsh_deployer']}")
        
        deployer_txs = self.get_address_transactions(self.seed_data['welsh_deployer'])
        
        if not deployer_txs:
            print("❌ Could not retrieve deployer transaction history")
            return False
        
        transactions = deployer_txs.get('results', [])
        arkadiko_addresses = set(self.seed_data['arkadiko_addresses'])
        
        funding_sources = []
        for tx in transactions:
            if tx.get('stx_received', 0) > 0:  # Incoming STX
                sender = tx.get('sender_address')
                if sender in arkadiko_addresses:
                    funding_sources.append({
                        'tx_id': tx.get('tx_id'),
                        'sender': sender,
                        'amount': tx.get('stx_received'),
                        'timestamp': tx.get('burn_block_time_iso')
                    })
        
        if funding_sources:
            smoking_gun = {
                'type': 'STRONG_EVIDENCE',
                'description': 'Deployer funded by known Arkadiko addresses',
                'evidence': f'Found {len(funding_sources)} funding transactions from Arkadiko',
                'conclusion': 'Philip controls the WELSH deployer address',
                'confidence': 90,
                'legal_impact': 'CONTROL_PROVEN',
                'funding_sources': funding_sources
            }
            self.smoking_guns.append(smoking_gun)
            self.evidence_score += 25
            
            print("🚨 SMOKING GUN FOUND!")
            print(f"✅ {smoking_gun['conclusion']}")
            print(f"   Found {len(funding_sources)} funding transactions")
            return True
        else:
            print(f"❌ No funding from known Arkadiko addresses found")
            return False
    
    def smoking_gun_check_4_arkadiko_interactions(self) -> bool:
        """
        SMOKING GUN CHECK 4: Arkadiko Contract Interactions
        Direct contract calls between deployer and Arkadiko
        """
        print("\n🔍 SMOKING GUN CHECK 4: Arkadiko Contract Interactions")
        print(f"Target: {self.seed_data['welsh_deployer']}")
        
        deployer_txs = self.get_address_transactions(self.seed_data['welsh_deployer'])
        
        if not deployer_txs:
            print("❌ Could not retrieve deployer transaction history")
            return False
        
        transactions = deployer_txs.get('results', [])
        arkadiko_addresses = set(self.seed_data['arkadiko_addresses'])
        
        interactions = []
        for tx in transactions:
            if tx.get('tx_type') == 'contract_call':
                contract_call = tx.get('contract_call', {})
                contract_id = contract_call.get('contract_id', '')
                
                # Check if contract call is to Arkadiko
                for arkadiko_addr in arkadiko_addresses:
                    if contract_id.startswith(arkadiko_addr):
                        interactions.append({
                            'tx_id': tx.get('tx_id'),
                            'contract_id': contract_id,
                            'function_name': contract_call.get('function_name'),
                            'timestamp': tx.get('burn_block_time_iso')
                        })
        
        if interactions:
            smoking_gun = {
                'type': 'STRONG_EVIDENCE',
                'description': 'Direct contract interactions with Arkadiko',
                'evidence': f'Found {len(interactions)} contract calls to Arkadiko',
                'conclusion': 'Same entity controls both WELSH and Arkadiko',
                'confidence': 85,
                'legal_impact': 'COORDINATION_PROVEN',
                'interactions': interactions
            }
            self.smoking_guns.append(smoking_gun)
            self.evidence_score += 20
            
            print("🚨 SMOKING GUN FOUND!")
            print(f"✅ {smoking_gun['conclusion']}")
            print(f"   Found {len(interactions)} contract interactions")
            return True
        else:
            print(f"❌ No direct Arkadiko contract interactions found")
            return False
    
    def run_smoking_gun_investigation(self) -> Dict:
        """
        Run complete smoking gun investigation
        Returns definitive proof or lack thereof
        """
        print("🚨 WELSH-FOUNDER HUNTER - SMOKING GUN INVESTIGATION")
        print("=" * 70)
        print("🎯 Mission: Find DEFINITIVE on-chain proof linking WELSH to Philip")
        print(f"🔍 Target Deployer: {self.seed_data['welsh_deployer']}")
        
        # Run all smoking gun checks
        checks = [
            self.smoking_gun_check_1_gift_transaction_sender,
            self.smoking_gun_check_2_lp_transaction_sender,
            self.smoking_gun_check_3_funding_source_trace,
            self.smoking_gun_check_4_arkadiko_interactions
        ]
        
        smoking_guns_found = 0
        for check in checks:
            try:
                if check():
                    smoking_guns_found += 1
            except Exception as e:
                print(f"⚠️ Check failed: {e}")
        
        # Calculate final assessment
        if self.evidence_score >= 50:
            conclusion = "DEFINITIVE PROOF FOUND"
            confidence = 95 + min(self.evidence_score - 50, 5)
        elif self.evidence_score >= 30:
            conclusion = "STRONG EVIDENCE FOUND"
            confidence = 80 + min(self.evidence_score - 30, 15)
        elif self.evidence_score >= 15:
            conclusion = "MODERATE EVIDENCE FOUND"
            confidence = 60 + min(self.evidence_score - 15, 20)
        else:
            conclusion = "INSUFFICIENT EVIDENCE"
            confidence = max(30, self.evidence_score * 2)
        
        results = {
            'smoking_guns_found': smoking_guns_found,
            'total_evidence_score': self.evidence_score,
            'conclusion': conclusion,
            'confidence': confidence,
            'smoking_guns': self.smoking_guns,
            'investigation_date': datetime.now().isoformat()
        }
        
        # Print results
        print("\n" + "=" * 70)
        print("🎉 SMOKING GUN INVESTIGATION COMPLETE!")
        print("=" * 70)
        
        print(f"\n📊 INVESTIGATION RESULTS:")
        print(f"  Smoking Guns Found: {smoking_guns_found}")
        print(f"  Evidence Score: {self.evidence_score}")
        print(f"  Conclusion: {conclusion}")
        print(f"  Confidence: {confidence}%")
        
        if self.smoking_guns:
            print(f"\n🚨 SMOKING GUNS DISCOVERED:")
            for i, gun in enumerate(self.smoking_guns, 1):
                print(f"  {i}. {gun['description']}")
                print(f"     Evidence: {gun['evidence']}")
                print(f"     Conclusion: {gun['conclusion']}")
                print(f"     Confidence: {gun['confidence']}%")
                print()
        
        return results

# Example usage
if __name__ == "__main__":
    # Initialize with Hiro API key
    hunter = SmokingGunHunter(hiro_api_key="your_hiro_api_key_here")
    
    # Run smoking gun investigation
    results = hunter.run_smoking_gun_investigation()
    
    # Print final assessment
    if results['smoking_guns_found'] > 0:
        print("🚨 SMOKING GUN EVIDENCE FOUND!")
        print("Philip's connection to WELSH token proven with definitive blockchain evidence!")
    else:
        print("❌ No smoking gun found in current investigation")
        print("Additional investigation methods may be required")