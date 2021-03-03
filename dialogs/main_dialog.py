from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    PromptOptions,
)

from dialogs.expire_dialog import ExpireDialog

from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState


class MainDialog(ComponentDialog):
    menu = '''
    1.套餐介绍
    2.使用教程
    3.软件下载
    4.到期时间查询
    5.人工服务
    
    请回复对应的数字:
    '''

    def __init__(self, user_state: UserState):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(ExpireDialog(ExpireDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.menu_step,
                    self.exec_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__

    async def menu_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(self.menu)),
        )

    async def exec_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        choice = step_context.result
        if   choice == "1":
            await step_context.context.send_activity(MessageFactory.text("这里是套餐介绍"))
        elif choice == "2":
            await step_context.context.send_activity(MessageFactory.text("这里是使用教程"))
        elif choice == "3":
            await step_context.context.send_activity(MessageFactory.text("这里是软件下载"))
        elif choice == "4":
            return await step_context.begin_dialog(ExpireDialog.__name__)
        elif choice == "5":
            await step_context.context.send_activity(MessageFactory.text("这里是人工服务"))

        #await step_context.context.send_activity(MessageFactory.text("会话已结束，感谢您的使用\n发送任意内容重新进入主菜单"))
        #return await step_context.end_dialog()
        return await step_context.replace_dialog(MainDialog.__name__)