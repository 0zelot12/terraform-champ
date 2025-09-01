import tempfile
import subprocess
import os
import json


def terraform_apply(apply_command):
    subprocess.run(apply_command, cwd=os.getcwd(), check=True)
    
    
def terraform_show(plan_path):
    result = subprocess.run(
        ["terraform", "show", "-json", plan_path],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout


def terraform_plan():
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
        
        
def build_apply_command(resources_to_target, resources_to_replace):
    return [
        "terraform", 
        "apply"
    ] + [f"-target={r}" for r in resources_to_target] + [f"-replace={r}" for r in resources_to_replace]


def cleanup_plan(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted temporary plan file: {path}")
        
        
def contains_resource_change_actions(actions):
    return any(action in actions for action in ["create", "update", "delete"])


def parse_resources(raw_data, changed_only=False):
    data = json.loads(raw_data)
    resources = []
    for resource_change in data.get("resource_changes", []):
        if not changed_only or contains_resource_change_actions(resource_change["change"]["actions"]):
            resources.append(resource_change["address"])
    return resources
