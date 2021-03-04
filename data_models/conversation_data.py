class ConversationData:
    def __init__(
        self,
        timestamp: str = None,
        channel_id: str = None,
        prompted_for_user_name: bool = True,
        current_menu_level: int = 1,
    ):
        self.timestamp = timestamp
        self.channel_id = channel_id
        self.prompted_for_user_name = prompted_for_user_name
        self.current_menu_level = current_menu_level
