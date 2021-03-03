import re
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    AttachmentPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from utils.database import MyDB


class ExpireDialog(ComponentDialog):

    def __init__(self, user_state: UserState):
        super(ExpireDialog, self).__init__(ExpireDialog.__name__)

        #self.user_profile_accessor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.email_step,
                    self.query_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__

    async def email_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("请输入邮箱地址.")),
        )
    
    async def query_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if "<a>" in step_context.result:
            email = re.findall(r'<a.*?>(.*?)</a>', step_context.result)[0]
        else:
            email = step_context.result
        mydb = MyDB()
        sql_query = mydb.query("select expire_in from user where email = '" + email + "'")
        if sql_query:
            results = " ".join('%s' %id for id in sql_query)
            msg = "用户 " + email + " 的过期时间：" + results
        else:
            msg = "用户不存在."

        await step_context.context.send_activity(MessageFactory.text(msg))

        mydb.close()
        #await step_context.context.send_activity(MessageFactory.text("会话已结束，感谢您的使用\n发送任意内容重新进入主菜单"))
        return await step_context.end_dialog()
