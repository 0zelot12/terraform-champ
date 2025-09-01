import tempfile
import subprocess
import os
import json
import sys

def terraform_apply(apply_command):
    """
    Run terraform apply with the given command.
    
    Args:
        apply_command (list): The terraform apply command as a list of strings
        
    Raises:
        SystemExit: If terraform apply fails
    """
    try:
        print(f"🚀 Running: {' '.join(apply_command)}")
        result = subprocess.run(
            apply_command, 
            cwd=os.getcwd(), 
            check=True,
            capture_output=False,
            text=True
        )
        print("✅ Terraform apply completed successfully")
        if result.stdout:
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
        print("❌ Terraform apply failed!")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        sys.exit(1)
        
    except FileNotFoundError:
        print("❌ Terraform command not found. Please ensure Terraform is installed and in your PATH.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected error during terraform apply: {e}")
        sys.exit(1)


def terraform_init(path, upgrade=False):
    """
    Run terraform init in the specified path.
    
    Args:
        path (str): The directory path where terraform init should be run
        upgrade (bool): Whether to upgrade modules and plugins
        
    Raises:
        SystemExit: If terraform init fails
    """
    init_command = ["terraform", "init", "-upgrade=true"] if upgrade else ["terraform", "init"]
    
    try:
        print(f"🔄 Running: {' '.join(init_command)} in 📂 {path}")
        result = subprocess.run(
            init_command, 
            cwd=path, 
            check=True,
            capture_output=False,
            text=True
        )
        print(f"✅ Terraform init completed successfully in 📂 {path}")
        if result.stdout:
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Terraform init failed in {path}!")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        sys.exit(1)
        
    except FileNotFoundError:
        print("❌ Terraform command not found. Please ensure Terraform is installed and in your PATH.")
        sys.exit(1)
        
    except OSError as e:
        print(f"❌ Error accessing directory 📂 {path}: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected error during terraform init in 📂 {path}: {e}")
        sys.exit(1)


def terraform_show(plan_path):
    """
    Run terraform show to get JSON output of a plan file.
    
    Args:
        plan_path (str): Path to the terraform plan file
        
    Returns:
        str: JSON output from terraform show
        
    Raises:
        SystemExit: If terraform show fails
    """
    try:
        print(f"🔍 Reading terraform plan from {plan_path}")
        result = subprocess.run(
            ["terraform", "show", "-json", plan_path],
            capture_output=True,
            text=True,
            check=True
        )
        print("✅ Successfully read terraform plan")
        return result.stdout
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Terraform show failed for plan file {plan_path}!")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        sys.exit(1)
        
    except FileNotFoundError:
        print("❌ Terraform command not found. Please ensure Terraform is installed and in your PATH.")
        sys.exit(1)
        
    except OSError as e:
        print(f"❌ Error accessing plan file {plan_path}: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected error during terraform show: {e}")
        sys.exit(1)


def terraform_plan():
    """
    Run terraform plan and return the path to the plan file.
    
    Returns:
        str: Path to the plan file
        
    Raises:
        SystemExit: If terraform plan fails
    """
    with tempfile.NamedTemporaryFile(suffix=".tfplan", delete=False) as tmp:
        plan_path = tmp.name
    try:
        print("🔄 Running terraform plan...")
        result = subprocess.run(
            ["terraform", "plan", f"-out={plan_path}"],
            cwd=os.getcwd(),
            check=True,
            capture_output=False,
            text=True
        )
        print("✅ Terraform plan completed successfully")
        return plan_path
    
    except subprocess.CalledProcessError as e:
        try:
            os.unlink(plan_path)
        except OSError:
            pass
        print("❌ Terraform plan failed!")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        sys.exit(1)
        
    except FileNotFoundError:
        try:
            os.unlink(plan_path)
        except OSError:
            pass
        print("❌ Terraform command not found. Please ensure Terraform is installed and in your PATH.")
        sys.exit(1)
        
    except Exception as e:
        try:
            os.unlink(plan_path)
        except OSError:
            pass
        print(f"❌ Unexpected error during terraform plan: {e}")
        sys.exit(1)
        
        
def build_apply_command(resources_to_target, resources_to_replace):
    return (
        ["terraform", "apply"] +
        [f"-target={r}" for r in resources_to_target] +
        [f"-replace={r}" for r in resources_to_replace]
    )


def cleanup_plan(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted temporary plan file: {path}")
        
        
def contains_resource_change_actions(actions):
    return any(action in actions for action in ["create", "update", "delete"])


def parse_resources(raw_data, changed_only=False, filter=None):
    data = json.loads(raw_data)
    resources = []
    for resource_change in data.get("resource_changes", []):
        if not changed_only or contains_resource_change_actions(resource_change["change"]["actions"]):
            resources.append(resource_change["address"])
        if filter:
            resources = [r for r in resources if filter in r]
    return resources
