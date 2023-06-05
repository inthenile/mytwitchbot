from pathlib import Path
import json

import twitchio


class Score:
    scoreboard = {}
    path = Path("Scores/scores.json")

    def __init__(self, user):
        """initiate the class with the user's name"""
        self.user = user

    async def update_score(self, new_score):
        """Store the score associated with the user"""
        # if the json file already exists,
        # read from it, update the dictionary,
        # and then turn it into a json again.
        if self.path.exists():
            old_content = self.path.read_text()
            data = json.loads(old_content)
            self.scoreboard.update(data)
            # if the user is already in the list, increment their score, else add them to the list.
            if self.user in self.scoreboard:
                self.scoreboard[self.user] += new_score
            else:
                self.scoreboard[self.user] = new_score
            print(self.scoreboard)
            contents = json.dumps(self.scoreboard, indent=4)
            with self.path.open("w") as file:
                file.write(contents)
                file.close()
        # create a fresh json file if none already exists
        else:
            self.scoreboard[self.user] = new_score
            contents = json.dumps(self.scoreboard, indent=4)
            with self.path.open("w") as file:
                file.write(contents)
                file.close()

    async def get_score(self, user):
        """ read the score of the user that is passed as the parameter from the .json file"""
        contents = self.path.read_text()
        score_log = json.loads(contents)
        # goes through the json searching for saved users and their points
        # returns None if they have 0 points
        for key, value in score_log.items():
            if key == user:
                return value
