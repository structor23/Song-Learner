class Song:
    def __init__(self, name):
        self.name = name
        self.last_evaluation = None
        self.overall_rating = 0
        self.criteria = {
            "Gesang": {
                "Textsicherheit": 0,
                "Timing": 0,
                "Intonation": 0,
                "Ausdruck": 0
            },
            "Gitarre": {
                "Arrangement": 0,
                "Technik": 0,
                "Timing": 0,
                "Ausdruck": 0
            },
            "Zusammenspiel": {
                "Timing": 0,
                "Dynamik": 0,
                "Bühnenpräsenz": 0,
                "Performance": 0
            }
        }