import questionary


def get_user_selection(choices, message):
    selected = questionary.checkbox(
        "Select the resources you want to apply changes to:", choices=choices
    ).ask()
    if selected is None:
        return []
    if len(selected) > 0:
        print("\n📝 Your selection:")
        for item in selected:
            print(f"- {item}")
    return selected