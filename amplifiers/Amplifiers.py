class MatchData:
    def __init__(self, amplifier_users, amplifier_id, team1, team2):
        self.amplifier_users = amplifier_users
        self.amplifier_id = amplifier_id
        self.team1 = team1
        self.team2 = team2
        self.teams = [team1, team2]

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


class DudeThatFingerlock(Amplifier):
    def __init__(self):
        super().__init__(1, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * min(1.15, 1 + (score.get_misses() / 200)))) for score in
         match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class LimitBreak(Amplifier):
    def __init__(self):
        super().__init__(2, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(score.get_combo()) for score in match.team1.get_player_scores()]
        [score.set_score(score.get_combo()) for score in match.team2.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class ColdClearEyesI(Amplifier):
    def __init__(self):
        super().__init__(3, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.05)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class ColdClearEyesIII(Amplifier):
    def __init__(self):
        super().__init__(4, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.15)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class ColdClearEyesII(Amplifier):
    def __init__(self):
        super().__init__(5, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.15)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class Gambler(Amplifier):
    def __init__(self):
        super().__init__(14, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.25)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class TheKingI(Amplifier):
    def __init__(self):
        super().__init__(15, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.9)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class TheKingII(Amplifier):
    def __init__(self):
        super().__init__(16, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 2)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class TheKingIII(Amplifier):
    def __init__(self):
        super().__init__(17, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 2)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class MakeItRock(Amplifier):
    def __init__(self):
        super().__init__(18, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        set_team = match.team2 if match.amplifier_users == match.team1 else match.team1
        [score.set_score(round(score.get_score() * 1.25)) for score in set_team.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class YinAndYangI(Amplifier):
    def __init__(self):
        super().__init__(20, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        def get_team_info(team):
            highest_score_player = max(team.get_player_scores(), key=lambda player_score: player_score.get_score(),
                                       default=None)
            highest_score_index = team.get_player_scores().index(highest_score_player)
            acc = team.get_player_scores()[1 - highest_score_index].get_acc()
            multiplier = 1.05 if team == match.amplifier_users else 1.0
            return round(highest_score_player.get_score() * acc / 100 * multiplier)

        team1_score = get_team_info(match.team1)
        team2_score = get_team_info(match.team2)

        return team1_score, team2_score


class YinAndYangII(Amplifier):
    def __init__(self):
        super().__init__(21, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        def get_team_info(team):
            highest_score_player = max(team.get_player_scores(), key=lambda player_score: player_score.get_score(),
                                       default=None)
            highest_score_index = team.get_player_scores().index(highest_score_player)
            acc = team.get_player_scores()[1 - highest_score_index].get_acc()
            multiplier = 1.1 if team == match.amplifier_users else 1.0
            return round(highest_score_player.get_score() * acc / 100 * multiplier)

        team1_score = get_team_info(match.team1)
        team2_score = get_team_info(match.team2)

        return team1_score, team2_score


class YinAndYangIII(Amplifier):
    def __init__(self):
        super().__init__(22, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        def get_team_info(team):
            highest_score_player = max(team.get_player_scores(), key=lambda player_score: player_score.get_score(),
                                       default=None)
            highest_score_index = team.get_player_scores().index(highest_score_player)
            acc = team.get_player_scores()[1 - highest_score_index].get_acc()
            multiplier = 1.1 if team == match.amplifier_users else 1.0
            return round(highest_score_player.get_score() * acc / 100 * multiplier)

        team1_score = get_team_info(match.team1)
        team2_score = get_team_info(match.team2)

        return team1_score, team2_score


class ClassicFarmerI(Amplifier):
    def __init__(self):
        super().__init__(25, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.05)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class ClassicFarmerII(Amplifier):
    def __init__(self):
        super().__init__(26, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.05)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class SynchronisedI(Amplifier):
    def __init__(self):
        super().__init__(28, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        base_multiplier = 1.1
        acc_difference = abs(match.amplifier_users.get_player_scores()[0].get_acc() -
                             match.amplifier_users.get_player_scores()[1].get_acc())
        if acc_difference >= 2:
            base_multiplier = 1.0
        else:
            base_multiplier -= 0.05 * acc_difference
        [score.set_score(round(score.get_score() * base_multiplier)) for score in
         match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class SynchronisedII(Amplifier):
    def __init__(self):
        super().__init__(29, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        base_multiplier = 1.2
        acc_difference = abs(match.amplifier_users.get_player_scores()[0].get_acc() -
                             match.amplifier_users.get_player_scores()[1].get_acc())
        if acc_difference >= 4:
            base_multiplier = 1.0
        else:
            base_multiplier -= 0.05 * acc_difference
        [score.set_score(round(score.get_score() * base_multiplier)) for score in
         match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class GoWithTheFlow(Amplifier):
    def __init__(self):
        super().__init__(30, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.15)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class LoadbearerI(Amplifier):
    def __init__(self):
        super().__init__(31, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        score_difference = match.amplifier_users.get_player_scores()[0].get_score() - \
                           match.amplifier_users.get_player_scores()[1].get_score()
        score_added = score_difference * 0.25

        if match.amplifier_users == match.team1:
            return round(match.team1.get_score() + score_added), match.team2.get_score()
        else:
            return match.team1.get_score(), round(match.team2.get_score() + score_added)


class LoadbearerII(Amplifier):
    def __init__(self):
        super().__init__(32, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        score_difference = match.amplifier_users.get_player_scores()[0].get_score() - \
                           match.amplifier_users.get_player_scores()[1].get_score()
        score_added = score_difference * 0.5

        if match.amplifier_users == match.team1:
            return round(match.team1.get_score() + score_added), match.team2.get_score()
        else:
            return match.team1.get_score(), round(match.team2.get_score() + score_added)


class LoadbearerIII(Amplifier):
    def __init__(self):
        super().__init__(33, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        score_difference = match.amplifier_users.get_player_scores()[0].get_score() - \
                           match.amplifier_users.get_player_scores()[1].get_score()
        score_added = score_difference * 0.5

        if match.amplifier_users == match.team1:
            return round(match.team1.get_score() + score_added), match.team2.get_score()
        else:
            return match.team1.get_score(), round(match.team2.get_score() + score_added)


class TrueHero(Amplifier):
    def __init__(self):
        super().__init__(36, 3)

    def get_modified_score(self, match: MatchData) -> (int, int):
        highest_score_player = max(match.amplifier_users.get_player_scores(),
                                   key=lambda player_score: player_score.get_score())

        highest_score_player.set_score(highest_score_player.get_score() * 1.3)
        return match.team1.get_score(), match.team2.get_score()


class TheDragonConsumesI(Amplifier):
    def __init__(self):
        super().__init__(37, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.1)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class TheDragonConsumesII(Amplifier):
    def __init__(self):
        super().__init__(38, 1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.2)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


class TheDragonConsumesIII(Amplifier):
    def __init__(self):
        super().__init__(39, 2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round(score.get_score() * 1.2)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()
