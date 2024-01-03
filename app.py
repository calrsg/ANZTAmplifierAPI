import json
from flask import Flask, jsonify, request
from amplifiers.Amplifiers import *

app = Flask(__name__)


# Load player/team/amplifier data
with open("data.json", "r") as f:
    data = json.load(f)

# ADD AMPLIFIERS HERE WHEN DONE :)
# The number is the amplifier ID
amplifiers = {
    0: Boost(),
    1: DudeThatFingerlock(),
    2: LimitBreak(),
    3: ColdClearEyesI(),
    4: ColdClearEyesII(),
    5: ColdClearEyesIII(),
    6: Gambler(),
    7: TheKingI(),
    8: TheKingII(),
    9: TheKingIII(),
    10: MakeItRock(),
    11: YinAndYangI(),
    12: YinAndYangII(),
    13: YinAndYangIII(),
    14: ClassicFarmerI(),
    15: ClassicFarmerII(),
    16: SynchronisedI(),
    17: SynchronisedII(),
    18: GoWithTheFlow(),
    19: LoadbearerI(),
    20: LoadbearerII(),
    21: LoadbearerIII(),
    22: TheDragonConsumesI(),
    23: TheDragonConsumesII(),
    24: TheDragonConsumesIII(),
    25: TrueHero()
}


@app.route('/score')
def score():
    # Retrieve query parameters (Flask didn't like the default values)
    team_name = request.args.get('team_name')
    amplifier_id = request.args.get('amplifier_id')
    player1_id = request.args.get('player1_id')
    player1_score = request.args.get('player1_score')
    player1_combo = request.args.get('player1_combo')
    player1_acc = request.args.get('player1_acc')
    player1_misses = request.args.get('player1_misses')

    player2_id = request.args.get('player2_id')
    player2_score = request.args.get('player2_score')
    player2_combo = request.args.get('player2_combo')
    player2_acc = request.args.get('player2_acc')
    player2_misses = request.args.get('player2_misses')

    player3_id = request.args.get('player3_id')
    player3_score = request.args.get('player3_score')
    player3_combo = request.args.get('player3_combo')
    player3_acc = request.args.get('player3_acc')
    player3_misses = request.args.get('player3_misses')

    player4_id = request.args.get('player4_id')
    player4_score = request.args.get('player4_score')
    player4_combo = request.args.get('player4_combo')
    player4_acc = request.args.get('player4_acc')
    player4_misses = request.args.get('player4_misses')

    # Convert params to right type
    player1_id, player2_id, player3_id, player4_id = int(player1_id), int(player2_id), int(player3_id), int(player4_id)
    player1_score, player2_score, player3_score, player4_score = int(player1_score), int(player2_score), int(player3_score), int(player4_score)
    player1_combo, player2_combo, player3_combo, player4_combo = int(player1_combo), int(player2_combo), int(player3_combo), int(player4_combo)
    player1_acc, player2_acc, player3_acc, player4_acc = float(player1_acc), float(player2_acc), float(player3_acc), float(player4_acc)
    player1_misses, player2_misses, player3_misses, player4_misses = int(player1_misses), int(player2_misses), int(player3_misses), int(player4_misses)
    amplifier_id = int(amplifier_id)

    # Data > objects (for sanity)
    p1 = PlayerScore(player1_id, player1_score, player1_combo, player1_acc, player1_misses)
    p2 = PlayerScore(player2_id, player2_score, player2_combo, player2_acc, player2_misses)
    team1 = Team([p1, p2])

    p3 = PlayerScore(player3_id, player3_score, player3_combo, player3_acc, player3_misses)
    p4 = PlayerScore(player4_id, player4_score, player4_combo, player4_acc, player4_misses)
    team2 = Team([p3, p4])

    # Determine which players belong to the given team
    team_players = data["teams"].get(team_name)
    if team_players is None:
        return jsonify({"error": "Team not found"}), 404

    # Identify the team for the amplifier
    amplifier_users = team1 if player1_id in team_players or player2_id in team_players else team2
    match = MatchData(amplifier_users, amplifier_id, team1, team2)

    # Find the corresponding amplifier instance
    amplifier = amplifiers.get(amplifier_id)
    if amplifier is None:
        return jsonify({"error": "Invalid amplifier ID"}), 404

    modified_scores = amplifier.get_modified_score(match)

    return jsonify(
        {
            "team1_score":  modified_scores[0],
            "team2_score":  modified_scores[1],
        })


if __name__ == '__main__':
    app.run()
