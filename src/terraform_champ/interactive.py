import questionary


def get_user_selection(choices, message):
    selected = questionary.checkbox(message=message, choices=choices).ask()
    if selected is None:
        return []
    if len(selected) > 0:
        print("\n📝 Your selection:")
        for item in selected:
            print(f"- {item}")
    return selected