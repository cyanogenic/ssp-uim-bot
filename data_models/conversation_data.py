class ConversationData:
    def __init__(
        self,
        timestamp: str = None,
        channel_id: str = None,
        current_menu_level: int = 1,
        query_lock: int = 0,
    ):
        self.timestamp = timestamp
        self.channel_id = channel_id
        self.current_menu_level = current_menu_level
        self.query_lock = query_lock
