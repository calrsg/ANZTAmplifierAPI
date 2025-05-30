# ANZT Amplifier API

_An API for calculating the score-modifying **amplifiers** used in **ANZT 11 Summer**, an Australian and New Zealand osu! tournament._

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Licence](https://img.shields.io/badge/Licence-MIT-lightgrey)](#licence)

## What’s this for?  
During ANZT 11 Summer each 2-player team can equip exactly **one amplifier** that tweaks how their in-game scores are evaluated.  
This micro-service:

* stores the full list of available amplifiers the calculations,
* exposes lightweight HTTP endpoints to calculate an adjusted score, and  
* serves a small helper endpoint for tournament tooling / overlays.

At tournament time the service is called live by the gosu! live stream client to display live modified scores to viewers, and also called retroactively via a Discord bot to examine the final scores of a match.

---
## What are amplifiers?

Amplifiers are Team Fight Tactics styled augments designed to revitalize standard osu! tournaments through adding unique effects and scoring. Some effects are quite simple, such as picking the map from a previous week of the tournament, while others have more unique effects such as adding a percentage to the score for each miss a team has. This API exists to simplify the usage of those in the latter category.

A full list of amplifiers for ANZT 11 Summer can be found [here](https://docs.google.com/spreadsheets/d/1RWuqemRanJGwpT9H1fiRNz0g8chFhmRNRNDzgR4Kstc/edit?gid=1207981974#gid=1207981974). These were designed based on feedback and learnings from ANZT 10 Summer to create a streamlined yet unique experience for players and staff.

## How it works

### `data.json` – the team register
`data.json` holds every registered **2-player** team in the format:

```json
{
  "Team Name": [ osu_id_1, osu_id_2 ],
  "Another Team": [ 1234567, 7654321 ]
}
```
These teams are used when player data is fed in, as the data fetched from osu! multiplayer lobbies is not sorted by teams. These team lists allow the API to sort the incoming scores into two pairs of valid teams before score calculations begin, and then return the scores on a per team basis.

### `amplifiers.py` - active amplifiers
`amplifiers.py` holds every active amplifier. Each amplifier has an ID and a number of uses set on initialization. 
All amplifiers have a `get_modified_score()` method that calculates a score based on the effect of the amplifier.
