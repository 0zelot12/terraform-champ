import os

def find_main_tf_files(start_path=".", excluded_dirs={}):
    main_tf_paths = []
    default_excluded_dirs = {'.terraform', 'node_modules'}
    merged_exluded_dirs = default_excluded_dirs.union(excluded_dirs)
    
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in merged_exluded_dirs]
        if "main.tf" in files:
            main_tf_paths.append(os.path.join(root, "main.tf"))
    
    return main_tf_paths

