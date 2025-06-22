#!/usr/bin/env python3
"""
WELSH-Founder Hunter CLI Tool
Command-line interface for blockchain forensics investigation
"""

import argparse
import json
import sys
import os
from welsh_hunter import WELSHFounderHunter, create_welsh_hunter_config

def main():
    parser = argparse.ArgumentParser(
        description="WELSH-Founder Hunter CLI - Blockchain forensics for WELSH token founder identification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli_tool.py --welsh-contract SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token \\
                     --arkadiko-wallets SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR \\
                     --output investigation_report.md

  python cli_tool.py --welsh-contract SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.welsh-token \\
                     --arkadiko-wallets SP2C2YFP12AJZB4MABJBAJ55XECVS7E4PMMZ89YZR \\
                     --philip-wallets SP1Y5YSTAHZ88XYK1VPDH24GY0HPX5J4JECTMY4A1 \\
                     --format json --output results.json
        """
    )
    
    parser.add_argument("--welsh-contract", required=True,
                       help="WELSH token contract address")
    parser.add_argument("--arkadiko-wallets", nargs="+", required=True,
                       help="Arkadiko wallet addresses")
    parser.add_argument("--philip-wallets", nargs="*",
                       help="Known Philip wallet addresses")
    parser.add_argument("--config", type=str,
                       help="Configuration file path (JSON)")
    parser.add_argument("--output", type=str, default="welsh_investigation_report.md",
                       help="Output report file (default: welsh_investigation_report.md)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown",
                       help="Output format (default: markdown)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show configuration and exit without running investigation")
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        if not os.path.exists(args.config):
            print(f"❌ Configuration file not found: {args.config}")
            sys.exit(1)
        
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in configuration file: {e}")
            sys.exit(1)
    else:
        config = create_welsh_hunter_config()
    
    # Load environment variables
    env_vars = [
        'HIRO_API_KEY', 'DISCORD_BOT_TOKEN', 'GITHUB_PAT',
        'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'
    ]
    
    for var in env_vars:
        if var in os.environ:
            config[var.lower()] = os.environ[var]
    
    if args.verbose:
        print("🔧 Configuration:")
        for key, value in config.items():
            if 'key' in key.lower() or 'token' in key.lower():
                display_value = f"{value[:8]}..." if value else "Not set"
            else:
                display_value = value
            print(f"  {key}: {display_value}")
        print()
    
    if args.dry_run:
        print("🏃 Dry run mode - configuration loaded successfully")
        print(f"📄 Would save results to: {args.output}")
        print(f"📊 Output format: {args.format}")
        sys.exit(0)
    
    # Initialize hunter
    try:
        hunter = WELSHFounderHunter(config)
    except Exception as e:
        print(f"❌ Failed to initialize WELSH-Founder Hunter: {e}")
        sys.exit(1)
    
    # Run investigation
    print("🚀 Starting WELSH-Founder Hunter investigation...")
    print(f"🎯 Target contract: {args.welsh_contract}")
    print(f"🏦 Arkadiko wallets: {len(args.arkadiko_wallets)}")
    if args.philip_wallets:
        print(f"👤 Philip wallets: {len(args.philip_wallets)}")
    print()
    
    try:
        result = hunter.run_full_investigation(
            welsh_contract=args.welsh_contract,
            arkadiko_wallets=args.arkadiko_wallets,
            philip_wallets=args.philip_wallets
        )
    except Exception as e:
        print(f"❌ Investigation failed: {e}")
        sys.exit(1)
    
    # Output results
    try:
        if args.format == "json":
            output_data = {
                "investigation_result": result,
                "timestamp": hunter.mission_state,
                "configuration": {
                    "welsh_contract": args.welsh_contract,
                    "arkadiko_wallets": args.arkadiko_wallets,
                    "philip_wallets": args.philip_wallets
                }
            }
            
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2, default=str)
        else:
            with open(args.output, 'w') as f:
                f.write(result.get('report', 'No report generated'))
        
        print(f"📄 Report saved to: {args.output}")
        
    except Exception as e:
        print(f"❌ Failed to save report: {e}")
        sys.exit(1)
    
    # Display summary
    print("\n" + "="*60)
    print("🎉 Investigation Complete!")
    print(f"🎯 Conclusion: {result.get('conclusion', 'Unknown')}")
    print(f"📊 Confidence: {result.get('confidence_score', 0):.1f}%")
    print(f"🔍 Evidence items: {result.get('evidence_count', 0)}")
    print(f"🕸️ Cluster size: {result.get('cluster_size', 0)} addresses")
    
    if result.get('success'):
        print("✅ Investigation completed successfully")
        sys.exit(0)
    else:
        print(f"❌ Investigation failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()