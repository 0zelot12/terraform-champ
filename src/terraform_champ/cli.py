import os

from .interactive import get_user_selection

from .file_utils import find_main_tf_files
from .terraform_utils import (
    terraform_plan,
    terraform_apply,
    terraform_show,
    terraform_init,
    terraform_state_list,
    parse_resources,
    parse_resources_from_str,
    build_apply_command,
    cleanup_plan
)

def apply_with_targets():
    plan_path = None
    try:
        plan_path = terraform_plan()
        
        plan_data = terraform_show(plan_path)
        changed_resources = parse_resources(plan_data, changed_only=True)
        
        if len(changed_resources) == 0:
            print("⚠️ No changes to apply detected...")
            return
            
        selected_resources = get_user_selection(changed_resources, "Select the resources you want to target:")
        if len(selected_resources) == 0:
            print("⚠️ No resources selected...")
            return
            
        apply_command = build_apply_command(selected_resources, [])
        terraform_apply(apply_command)
        
    except Exception as e:
        print(f"❌ Error during apply_with_targets: {e}")
        raise
    finally:
        if plan_path:
            cleanup_plan(plan_path)
        

def apply_with_replacements(filter):
    try:
        resource_data = terraform_state_list()
        all_resources = parse_resources_from_str(resource_data, filter=filter)
        
        selected_resources = get_user_selection(all_resources, "Select the resources you want to replace:")
        if len(selected_resources) == 0:
            print("⚠️ No resources selected...")
            return
        
        apply_command = build_apply_command([], selected_resources)
        terraform_apply(apply_command)
        
    except Exception as e:
        print(f"❌ Error during apply_with_replacements: {e}")
        raise
        
def init(upgrade=False):
    try:
        main_tf_paths = find_main_tf_files(
            start_path=os.getcwd(),
            excluded_dirs={"management", "performance-testing-cluster"}
        )
        selected_paths = get_user_selection(main_tf_paths, "Select the paths you want to init:")
        if len(selected_paths) == 0:
            print("⚠️ No paths selected...")
            return
        for path in selected_paths:
            command_str = "terraform init"
            if upgrade:
                command_str += " --upgrade"
            terraform_init(path, upgrade=upgrade)
    except Exception as e:
        print(f"❌ Error during run_init: {e}")
        raise