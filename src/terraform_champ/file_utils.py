import os


def get_excluded_directories():
    # TODO: Add error handling
    # TODO: Is there a way to do this on a project level rather than setting it globally?
    excluded_dirs_str = os.environ.get('TFCHAMP_EXCLUDED_DIRS')
    if excluded_dirs_str:
        print(f"⚙️ TFCHAMP_EXCLUDED_DIRS: {excluded_dirs_str}")
        return {
            d.strip()
            for d in excluded_dirs_str.split(',')
            if d.strip()
        }
    else: 
        print(f"⚙️ TFCHAMP_EXCLUDED_DIRS not set")
        return set()


def find_main_tf_files(start_path="."):
    main_tf_paths = []
    
    default_excluded_dirs = {'.terraform', 'node_modules'}
    
    user_excluded_dirs = get_excluded_directories()
    merged_excluded_dirs = default_excluded_dirs.union(user_excluded_dirs)
    
    print("🚫 Excluded directories:")
    for d in sorted(merged_excluded_dirs):
        print(f" - {d}")
    
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in merged_excluded_dirs]
        if "main.tf" in files:
            main_tf_paths.append(os.path.join(root))
    
    return main_tf_paths

