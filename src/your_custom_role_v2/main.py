#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
import agentops
from starlette.middleware.cors import CORSMiddleware

from your_custom_role_v2.CrewCustomHandler import reply
from your_custom_role_v2.crew import YourCustomRoleV2
from fastapi import FastAPI

from your_custom_role_v2.entity.WebEntity import RoleInput

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'username': 'xuhongzhuo',
        'custom_role': '男朋友',
        'user_input': '想我了吧？'
    }

    try:
        YourCustomRoleV2().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        YourCustomRoleV2().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        YourCustomRoleV2().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        YourCustomRoleV2().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中建议设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

@app.get("/test-info")
def read_test_info():
    return {"hello": "world"}


"""
角色扮演的回答就在这里
"""


@app.post("/role-play-reply")
def rol_play_reply(inputs: RoleInput):
    res_str = reply(inputs.username,
                 inputs.role,
                 inputs.input_dialog)
    return {
        "res":res_str
    }


