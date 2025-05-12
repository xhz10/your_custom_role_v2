#!/usr/bin/env python
import asyncio
import json
import os
import select
import signal
import subprocess
import sys
import threading
import time
import uuid
import warnings
from fastapi import FastAPI, Request

from typing import Dict, Any, Optional

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from your_custom_role_v2.CrewCustomHandler import reply
from your_custom_role_v2.crew import YourCustomRoleV2
from fastapi import FastAPI, Depends, Cookie

from your_custom_role_v2.entity.WebEntity import RoleInput, TrainRoleInput

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

# 存储活跃进程的字典
active_processes: Dict[str, Dict[str, Any]] = {}


# 清理过期进程的函数
def cleanup_old_processes():
    while True:
        current_time = time.time()
        to_remove = []

        for session_id, process_info in active_processes.items():
            # 如果进程超过30分钟未活动，终止它
            if current_time - process_info['last_activity'] > 30 * 60:
                try:
                    os.kill(process_info['process'].pid, signal.SIGTERM)
                    process_info['process'].terminate()
                except:
                    pass
                to_remove.append(session_id)

        # 从字典中移除已终止的进程
        for session_id in to_remove:
            del active_processes[session_id]

        time.sleep(60)  # 每分钟检查一次


# 启动清理线程
cleanup_thread = threading.Thread(target=cleanup_old_processes, daemon=True)
cleanup_thread.start()


async def get_session_id(request):
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())
    return request.session["session_id"]


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
        "res": res_str
    }


@app.post("/api/start_training")
async def start_training(request: Request):
    data = await request.json()

    config_json = {
        "username": data.get("username"),
        "custom_role": data.get("custom_role"),
        "user_input": data.get("user_input"),
        "iter_cnt": data.get("iter_cnt")
    }

    config_str = json.dumps(config_json)
    log_file_name = 'output.log'

    # 启动子进程，将stdout和stderr重定向到日志文件
    with open(log_file_name, 'w') as log_file:
        process = subprocess.Popen(
            ["python3", "TrainHandler.py", "--config", config_str],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True
        )

    async def sse_stream():
        with open(log_file_name, 'r') as log_file:
            log_file.seek(0, os.SEEK_END)  # 跳到文件末尾，读取最新内容

            while process.poll() is None:
                where = log_file.tell()
                line = log_file.readline()
                if not line:
                    log_file.seek(where)
                    await asyncio.sleep(0.1)
                else:
                    yield f"data: {line.strip()}\n\n"

            # After process is done, read the remaining content
            for line in log_file:
                yield f"data: {line.strip()}\n\n"

    return StreamingResponse(sse_stream(), media_type="text/event-stream")

    # 启动进程API
    # @app.post("/api/start_training")
    # async def start_training(
    #         params: TrainRoleInput
    #         #session_id: str = Depends(get_session_id)
    # ):
    #     # if session_id in active_processes:
    #     #     return {
    #     #         "status": "already_running",
    #     #         "initial_output": active_processes[session_id].get("initial_output", "")
    #     #     }
    #
    #     config_json = {
    #         "username": params.username,
    #         "custom_role": params.custom_role,
    #         "user_input": params.user_input,
    #         "iter_cnt": params.iter_cnt
    #     }
    #
    #     # 启动子进程
    #     process = subprocess.Popen(
    #         ["python", "TrainHandler.py", f"--config={config_json}"],
    #         stdin=subprocess.PIPE,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT,
    #         text=True,
    #         bufsize=1,
    #         universal_newlines=True
    #     )
    #
    #     # 读取初始输出（如果有）
    #     initial_output = ""
    #     readable, _, _ = select.select([process.stdout], [], [], 0.5)
    #     if readable:
    #         initial_output = process.stdout.readline()
    #         # 如果需要读取多行初始输出
    #         while select.select([process.stdout], [], [], 0.1)[0]:
    #             line = process.stdout.readline()
    #             if not line.strip():  # 空行表示初始输出结束
    #                 break
    #             initial_output += line

    # # 存储进程信息
    # active_processes[session_id] = {
    #     "process": process,
    #     "last_activity": time.time(),
    #     "initial_output": initial_output,
    #     "params": params.dict()
    # }

#
# return {
#     "status": "started",
#     "initial_output": initial_output,
#     "username": params.username,
#     "custom_role": params.custom_role
# }
