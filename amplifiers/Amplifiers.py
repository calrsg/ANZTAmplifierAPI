class MatchData:
    def __init__(self, amplifier_users, amplifier_id, team1, team2):
        self.amplifier_users = amplifier_users
        self.amplifier_id = amplifier_id
        self.team1 = team1
        self.team2 = team2

    def get_current_score(self):
        return sum(self.team1.get_players().get_score()), sum(self.team2.get_players().get_score())


class PlayerScore:
    def __init__(self, player_id: int, score: int, combo: int, acc: float, misses: int):
        self.player_id = player_id
        self.score = score
        self.combo = combo
        self.acc = acc
        self.misses = misses

    def get_id(self) -> int:
        return self.player_id

    def get_score(self) -> int:
        return self.score

    def get_combo(self) -> int:
        return self.combo

    def get_acc(self) -> float:
        return self.acc

    def get_misses(self) -> int:
        return self.misses

    def set_score(self, score: int):
        self.score = score

    def set_combo(self, combo: int):
        self.combo = combo

    def set_acc(self, acc: float):
        self.acc = acc

    def set_misses(self, misses: int):
        self.misses = misses


class Team:
    def __init__(self, players: [PlayerScore]):
        self.players = players

    def get_player_scores(self) -> [PlayerScore]:
        return self.players

    def get_player(self, player_id: int) -> PlayerScore:
        for player in self.players:
            if player.get_id() == player_id:
                return player
        raise ValueError(f"Player {player_id} not in team.")

    def get_score(self) -> [int]:
        return sum([player.get_score() for player in self.players])


class Amplifier:
    def __init__(self, amplifier_id: int, amplifier_uses: int):
        self.amplifier_id = amplifier_id
        self.amplifier_uses = amplifier_uses

    def get_modified_score(self, data: MatchData) -> (int, int):
        """
        :return: Current score of the match based on Amplifier effect
        """
        pass

    def get_id(self) -> int:
        return self.amplifier_id

    def get_uses(self) -> int:
        return self.amplifier_uses


class Boost(Amplifier):
    """
    TEST AMPLIFIER: Boosts using teams score by 30%
    """
    def __init__(self):
        super().__init__(0, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.3)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class DudeThatFingerlock(Amplifier):
    def __init__(self):
        super().__init__(1, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * (1 + (score.get_misses() / 200)))) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class LimitBreak(Amplifier):
    def __init__(self):
        super().__init__(2, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(score.get_combo()) for score in match.team1.get_player_scores()]
        [score.set_score(score.get_combo()) for score in match.team2.get_player_scores()]
        [score.set_score(round(score.get_score() * 1.01)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()

