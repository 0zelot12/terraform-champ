#!/usr/bin/env python3

import questionary
import subprocess
import os
import tempfile
import json

def cleanup_plan(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted temporary plan file: {path}")

def generate_plan():
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
    selected = questionary.checkbox(
        "Select the resources you want to apply changes to:",
        choices=choices
    ).ask()
    
    print("\n Running terraform apply targeting the following resources:")
    for item in selected:
        print(f"- {item}")

    return selected


def contains_resource_change_actions(actions):
    return any(action in actions for action in ["create", "update", "delete"])


def load_changed_resources(plan_path):
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
    target_args = []
    for resource in resources:
        target_args.append(f'-target={resource}')
    return ["terraform", "apply"] + target_args


def main():
    plan_path = generate_plan()
    changed_resources = load_changed_resources(plan_path)
    selected_resources = get_user_selection(changed_resources)
    apply_command = build_apply_command(selected_resources)
    subprocess.run(apply_command, cwd=os.getcwd(), check=True)
    cleanup_plan(plan_path)


if __name__ == "__main__":
    main()
