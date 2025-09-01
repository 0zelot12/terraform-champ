#!/usr/bin/env python3

import questionary
import argparse


from terraform_utils import (
    terraform_plan,
    terraform_apply,
    terraform_show,
    parse_resources,
    build_apply_command,
    cleanup_plan
)


def get_user_selection(choices):
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
        choices=["target", "replace"],
        help="Mode: 'target' for selective resource targeting, 'replace' for replace command",
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
        selected_resources = get_user_selection(changed_resources)
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

def apply_with_replacements():
    try:
        plan_path = terraform_plan()
        plan_data = terraform_show(plan_path)
        all_resources = parse_resources(plan_data)
        selected_resources = get_user_selection(all_resources)
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
    

def main():
    args = parse_arguments()
    if args.mode == "replace":
        apply_with_replacements()
    elif args.mode == "target":
        apply_with_targets()
    else:
        raise ValueError(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()
    