#!/usr/bin/env python3

import argparse


from terraform_champ.cli import apply_with_replacements, apply_with_targets, init, apply


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Interactive Terraform commands with resource selection 🚀"
    )
    
    subparsers = parser.add_subparsers(dest="mode", required=True, help="Available commands")

    # Target subcommand
    target_parser = subparsers.add_parser(
        "target",
        help="Selective resource targeting 🎯"
    )
    target_parser.add_argument(
        "--filter",
        type=str,
        help="Optional substring filter for resource addresses, e.g. --filter='xyz'"
    )

    # Replace subcommand
    replace_parser = subparsers.add_parser(
        "replace",
        help="Replace command 🔄"
    )
    replace_parser.add_argument(
        "--filter",
        type=str,
        help="Optional substring filter for resource addresses, e.g. --filter='xyz'"
    )

    # Init subcommand
    init_parser = subparsers.add_parser(
        "init",
        help="Run 'terraform init' in all relevant directories ⚡"
    )
    
    init_parser.add_argument(
            "--upgrade",
            action="store_true",
            help="Upgrade modules and plugins during terraform init ⬆️"
        )
    
    # Apply subcommand
    apply_parser = subparsers.add_parser(
        "apply",
        help="Run 'terraform apply' in all relevant directories ⚡"
    )
    
    apply_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="TODO"
    )
    
    apply_parser.add_argument(
        "--interactive",
        action="store_true",
        help="TODO"
    )

    return parser.parse_args()
    

def main():
    args = parse_arguments()
    if args.mode == "replace":
        apply_with_replacements(filter=args.filter)
    elif args.mode == "target":
        apply_with_targets()
    elif args.mode == "init":
        init(upgrade=args.upgrade)
    elif args.mode == "apply":
        apply(interactive=args.interactive, dry_run=args.dry_run)
    else:
        raise ValueError(f"Unknown mode: {args.mode}")
    
    
# TODO: Add proper logger with log levels


if __name__ == "__main__":
    main()
