"""
调教我这个角色
"""
import argparse
import json

from your_custom_role_v2.crew import YourCustomRoleV2


def train_role(username: str, custom_role: str, user_input: str, iter_cnt):
    """
        Run the crew.
        """
    inputs = {
        'username': username,
        'custom_role': custom_role,
        'user_input': user_input
    }
    file_name = './train_history/' + username + '/' + custom_role + '-train.pkl'
    try:
        YourCustomRoleV2().crew().train(n_iterations=iter_cnt, filename=file_name, inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='自定义角色训练')
    parser.add_argument('--config', help='JSON格式的配置参数')
    args = parser.parse_args()

    if args.config:
        try:
            config = json.loads(args.config)
            username = config.get('username', 'default_user')
            custom_role = config.get('custom_role', 'default_role')
            user_input = config.get('user_input')
            iter_cnt = config.get('iter_cnt')

            # 调用实际的训练函数
            train_role(username=username, custom_role=custom_role, user_input=user_input, iter_cnt=iter_cnt)
        except json.JSONDecodeError:
            print("错误: 无法解析JSON配置")
        except Exception as e:
            print(f"错误: {str(e)}")
    else:
        print("错误: 未提供配置")
