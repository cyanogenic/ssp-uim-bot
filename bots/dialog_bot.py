import json

from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from botbuilder.schema import ChannelAccount
from helpers.dialog_helper import DialogHelper

from data_models import ConversationData, UserProfile


class DialogBot(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.conversation_data_accessor = self.conversation_state.create_property(
            "ConversationData"
        )
        self.user_profile_accessor = self.user_state.create_property("UserProfile")
        self.dialog = dialog

        self.menu = json.load(open('conf/menu.json', 'r'))

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("欢迎使用!请发送任意内容进入菜单")
    
    async def on_message_activity(self, turn_context: TurnContext):
        user_profile = await self.user_profile_accessor.get(turn_context, UserProfile)
        conversation_data = await self.conversation_data_accessor.get(
            turn_context, ConversationData
        )

        if user_profile.name is None:
            # First time around this is undefined, so we will set recipient.id as username.
            user_profile.name = turn_context.activity.recipient.id
            conversation_data.channel_id = turn_context.activity.channel_id

        # 进查询
        if conversation_data.query_lock == 1:
            # 进瀑布对话
            await DialogHelper.run_dialog(self.dialog, turn_context, self.conversation_state.create_property("DialogState"))
            conversation_data.query_lock = 0
        else:
            # 判断输入是不是数字,否则菜单层级不变
            if turn_context.activity.text.isdigit():
                if int(turn_context.activity.text) == 4:
                    conversation_data.query_lock = 1
                    # 进瀑布对话
                    await DialogHelper.run_dialog(self.dialog, turn_context, self.conversation_state.create_property("DialogState"))
                else:
                    # 判断当前用户在哪一层
                    if int(turn_context.activity.text) < 100:
                        conversation_data.current_menu_level = 1
                    else:
                        conversation_data.current_menu_level = int(turn_context.activity.text) // 100 * 100

                    menu_temp = await self.create_menu(conversation_data.current_menu_level)           
                    # 发送菜单
                    await turn_context.send_activity(menu_temp)

                    await turn_context.send_activity(
                        f"{ user_profile.name } sent: { turn_context.activity.text } current level:{ conversation_data.current_menu_level }"
                    )

    async def create_menu(self, level):
        # 生成当前用户层级的菜单
        menu_temp = ''
        for key in self.menu:
            if int(key) >= level and int(key) < level + 99:
                menu_temp = menu_temp + "\n\n" + key + ": " + self.menu[key]
        # 补"返回上一层"
        if level > 1:
            menu_temp = menu_temp + "\n\n" + "0: 返回上一层"
        return menu_temp

