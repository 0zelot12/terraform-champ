#!/usr/bin/env python3

import questionary
import argparse
import os


from file_utils import find_main_tf_files
from terraform_utils import (
    terraform_plan,
    terraform_apply,
    terraform_show,
    terraform_init,
    parse_resources,
    build_apply_command,
    cleanup_plan
)


def get_user_selection(choices, message):
    selected = questionary.checkbox(
        "Select the resources you want to apply changes to:", choices=choices
    ).ask()
    if selected is None:
        return []
    if len(selected) > 0:
        print("\n Your selection:")
        for item in selected:
            print(f"- {item}")
    return selected


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Interactive Terraform apply with resource selection"
    )
    parser.add_argument(
        "mode",
        choices=["target", "replace" , "init"],
        help="Mode: 'target' for selective resource targeting, 'replace' for replace command",
    )
    parser.add_argument(
        "--filter",
        type=str,
        help="Optional substring filter for resource addresses, e.g. --filter='xyz'",
    )
    return parser.parse_args()


def apply_with_targets():
    try:
        plan_path = terraform_plan()
        plan_data = terraform_show(plan_path)
        changed_resources = parse_resources(plan_data, changed_only=True)
        if len(changed_resources) == 0:
            print("No changes to apply detected...")
            return
        selected_resources = get_user_selection(changed_resources, "Select the resources you want to target:")
        if len(selected_resources) == 0:
            print("No resources selected...")
            return
        apply_command = build_apply_command(selected_resources, [])
        terraform_apply(apply_command)
    except Exception as e:
        print(f"Error during apply_with_targets: {e}")
        raise
    finally:
        cleanup_plan(plan_path)
        

def apply_with_replacements(filter):
    try:
        plan_path = terraform_plan()
        plan_data = terraform_show(plan_path)
        all_resources = parse_resources(plan_data, filter=filter)
        selected_resources = get_user_selection(all_resources, "Select the resources you want to replace:")
        if len(selected_resources) == 0:
            print("No resources selected...")
            return
        apply_command = build_apply_command([], selected_resources)
        terraform_apply(apply_command)
    except Exception as e:
        print(f"Error during apply_with_replacements: {e}")
        raise
    finally:
        cleanup_plan(plan_path)
        
def init():
    try:
        main_tf_paths = find_main_tf_files(
            start_path=os.getcwd(),
            excluded_dirs={"management", "performance-testing-cluster"}
        )
        selected_paths = get_user_selection(main_tf_paths, "Select the paths you want to init:")
        for path in selected_paths:
            print(f"🚀 Running 'terraform init' in 📂 '{path}'")
            terraform_init(path)
    except Exception as e:
        print(f"❌ Error during run_init: {e}")
        raise
    

def main():
    args = parse_arguments()
    if args.mode == "replace":
        apply_with_replacements(filter=args.filter)
    elif args.mode == "target":
        apply_with_targets()
    elif args.mode == "init":
        init()
    else:
        raise ValueError(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()
