class RBUser:
    def __init__(self, user_id: int | None = None,
                 first_name: str | None = None):
        self.id = user_id
        self.first_name = first_name

    def to_dict(self) -> dict:
        data = {'id': self.id, 'first_name': self.first_name}
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data