from datetime import datetime


class AssetEvent:
    def __init__(self, title, description, event_type, created_by):
        self.title = title
        self.description = description
        self.event_type = event_type
        self.created_by = created_by
        self.created_at = datetime.now()