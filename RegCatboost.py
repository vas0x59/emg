import catboost

class RegCatboost:
    def __init__(self, url):
        self.clf = catboost.CatBoostClassifier()
        self.clf.load_model(url)

    def predict(self, data):
        p = self.clf.predict(data)
        return p