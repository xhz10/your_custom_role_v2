# 自定义监听器
from crewai.utilities.events import AgentExecutionStartedEvent
from crewai.utilities.events.base_event_listener import BaseEventListener


class MyCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(AgentExecutionStartedEvent)
        def on_crew_started(source, event):
            print(f'agent_task_prompt start : {event.task_prompt}')


