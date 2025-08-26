#!/usr/bin/env python3

import questionary
import subprocess
import os
import tempfile
import json
import argparse

def cleanup_plan(path):
    """
    Deletes the temporary Terraform plan file at the given path.
    Args:
        path (str): Path to the Terraform plan file.
    """
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted temporary plan file: {path}")

def generate_plan():
    """
    Generates a Terraform plan and saves it to a temporary file.
    Returns:
        str: The path to the generated Terraform plan file.
    """
    with tempfile.NamedTemporaryFile(suffix=".tfplan", delete=False) as tmp:
        plan_path = tmp.name
    try:
        subprocess.run(
            ["terraform", "plan", f"-out={plan_path}"],
            cwd=os.getcwd(),
            check=True
        )
        return plan_path
    except:
        print("Terraform plan failed, please check your configurations")

def get_user_selection(choices):
    """
    Prompts the user to select resources from a list of choices.
    Args:
        choices (list): List of resource addresses to choose from.
    Returns:
        list: List of selected resource addresses.
    """
    selected = questionary.checkbox(
        "Select the resources you want to apply changes to:",
        choices=choices
    ).ask()
   
    print("\n Running terraform apply targeting the following resources:")
    for item in selected:
        print(f"- {item}")
    return selected

def contains_resource_change_actions(actions):
    """
    Checks if a list of Terraform actions includes create, update, or delete.
    Args:
        actions (list): List of actions from a Terraform resource change.
    Returns:
        bool: True if any action is 'create', 'update', or 'delete', else False.
    """
    return any(action in actions for action in ["create", "update", "delete"])

def load_changed_resources(plan_path):
    """
    Loads resources from a Terraform plan that have changes to apply.
    Args:
        plan_path (str): Path to the Terraform plan file.
    Returns:
        list: List of resource addresses with pending changes.
    """
    result = subprocess.run(
        ["terraform", "show", "-json", plan_path],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(result.stdout)
    resources = []
    for resource_change in data.get("resource_changes", []):
        if contains_resource_change_actions(resource_change["change"]["actions"]):
            resources.append(resource_change["address"])
    return resources

def build_apply_command(resources):
    """
    Builds a Terraform apply command targeting the specified resources.
    Args:
        resources (list): List of resource addresses to target.
        
    Returns:
        list: Command list to execute with subprocess.
    """
    target_args = []
    for resource in resources:
        target_args.append(f'-target={resource}')
    return ["terraform", "apply"] + target_args

def parse_arguments():
    """
    Parses command line arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Interactive Terraform apply with resource selection")
    parser.add_argument(
        "mode", 
        choices=["target", "replace"],
        help="Mode: 'target' for selective resource targeting, 'replace' for replace command"
    )
    return parser.parse_args()

def apply_with_targets():
    plan_path = generate_plan()
    changed_resources = load_changed_resources(plan_path)
    selected_resources = get_user_selection(changed_resources)
    apply_command = build_apply_command(selected_resources)
    subprocess.run(apply_command, cwd=os.getcwd(), check=True)
    cleanup_plan(plan_path)
    

def main():
    """
    Main execution function.
    - Parses command line arguments
    - Generates a Terraform plan
    - Loads changed resources from the plan
    - Prompts the user to select which resources to apply
    - Executes `terraform apply` on the selected resources
    - Cleans up the temporary plan file
    """
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
