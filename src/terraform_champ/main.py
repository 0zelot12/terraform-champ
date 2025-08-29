#!/usr/bin/env python3

import questionary
import argparse


from terraform_utils import (
    terraform_plan,
    terraform_show,
    parse_changed_resources,
    build_apply_command,
    cleanup_plan,
    run_apply,
)


def get_user_selection(choices):
    selected = questionary.checkbox(
        "Select the resources you want to apply changes to:", choices=choices
    ).ask()

    print("\n Running terraform apply targeting the following resources:")
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
    plan_path = terraform_plan()
    plan_data = terraform_show(plan_path)
    changed_resources = parse_changed_resources(plan_data)
    selected_resources = get_user_selection(changed_resources)
    apply_command = build_apply_command([selected_resources], [])
    run_apply(apply_command)
    cleanup_plan(plan_path)

def apply_with_replacements():
    # TODO: Implement this function
    pass

def main():
    args = parse_arguments()
    if args.mode == "replace":
        print("REPLACE_MODE")
    elif args.mode == "target":
        apply_with_targets()
    else:
        raise ValueError(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()

# TODO: Make sure temp files get cleaned up, even if the script fails or the user cancels it
# TODO: Abort in case nothing is selected
# TODO: Add replace command