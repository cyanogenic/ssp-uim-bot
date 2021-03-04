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
            # First time around this is undefined, so we will prompt user for name.
            if conversation_data.prompted_for_user_name:
                # Set the name to what the user provided.
                user_profile.name = turn_context.activity.recipient.id
                conversation_data.channel_id = turn_context.activity.channel_id
                # Reset the flag to allow the bot to go though the cycle again.
                conversation_data.prompted_for_user_name = False
                
        await turn_context.send_activity(
            f"{ user_profile.name } sent: { turn_context.activity.text }"
        )

        #进瀑布对话
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
