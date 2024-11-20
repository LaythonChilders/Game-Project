import json

class Scoreboard:
    def __init__(self, player, filename="scores.json"):
        self.player = player
        self.score = player.score
        self.filename = filename
        self.scores = self.load_scores()

    def save_scores(self):
        """Save the top 10 scores to a JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.scores, file, indent=4)

    def load_scores(self):
            """
            Load scores from a JSON file. If the file doesn't exist, create it 
            with an empty list and return an empty scoreboard.
            """
            try:
                with open(self.filename, "r") as file:
                    return json.load(file)
            except FileNotFoundError:
                # Create the file with an empty list
                with open(self.filename, "w") as file:
                    json.dump([], file, indent=4)
                return []

    def add_score(self, initials, score):
        self.scores.append({"initials": initials, "score": score})
        
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        
        self.scores = self.scores[:10]
        
        self.save_scores()

    def get_scores(self):
        return self.scores
