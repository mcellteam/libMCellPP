class ModelPart:

    def __init__(self):
        self.subscribed_models = set()

    def add_model_to_subscribers(self, model):
        self.subscribed_models.add(model)

    def remove_model_from_subscribers(self, model):
        self.subscribed_models.discard(model)
