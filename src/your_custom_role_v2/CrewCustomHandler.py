from your_custom_role_v2.crew import YourCustomRoleV2


def reply(username:str,custom_role:str,user_input:str) -> str:
    """
    Run the crew.
    """
    inputs = {
        'username': username,
        'custom_role': custom_role,
        'user_input': user_input
    }

    try:
        output = YourCustomRoleV2().crew().kickoff(inputs=inputs)
        return output.raw
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train_role(username:str,custom_role:str,user_input:str):
    """
        Run the crew.
        """
    inputs = {
        'username': username,
        'custom_role': custom_role,
        'user_input': user_input
    }

    try:
        output = YourCustomRoleV2().crew().kickoff(inputs=inputs)
        return output.raw
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")