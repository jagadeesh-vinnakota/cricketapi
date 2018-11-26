from flask import *
import requests

# provides player information
def find_player_information(playerId):
    result_data = requests.get(
        'https://cricapi.com/api/playerStats?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2&pid={}'.format(playerId))
    return result_data.json()

#provides player biography
def find_player_biography(bio):
    if bio['data']:
        player_data = find_player_information(bio['data'][0]['pid'])
        player_biography = {}
        player_biography['country'] = player_data['country']
        player_biography['profile'] = player_data['profile']
        player_biography['imageURL'] = player_data['imageURL']
        player_biography['fullName'] = player_data['fullName']
        player_biography['born'] = player_data['born']
        player_biography['battingStyle'] = player_data['battingStyle']
        player_biography['bowlingStyle'] = player_data['bowlingStyle']
        player_biography['playingRole'] = player_data['playingRole']
        player_biography['majorTeams'] = player_data['majorTeams']
        return jsonify([player_biography])
    else:
        return jsonify([{"message":"Player Not Found"}]),404

# Provides the player statistics
def find_player_statistics(bio):
    if bio['data']:
        player_statistics = {}
        player_data = find_player_information(bio['data'][0]['pid'])

        bowling_statistics = {}
        bowling_statistics['listA'] = None
        bowling_statistics['firstClass'] = None
        bowling_statistics['T20Is'] = None
        bowling_statistics['ODIs'] = None
        bowling_statistics['tests'] = None

        batting_statistics = {}
        batting_statistics['listA'] = None
        batting_statistics['firstClass'] = None
        batting_statistics['T20Is'] = None
        batting_statistics['ODIs'] = None
        batting_statistics['tests'] = None

        for key in player_data['data']['bowling'].keys():
            bowling_statistics[key] = player_data['data']['bowling'][key]

        for key in player_data['data']['batting'].keys():
            batting_statistics[key] = player_data['data']['batting'][key]

        player_statistics['bowling']= bowling_statistics
        player_statistics['batting'] = batting_statistics

        return jsonify([player_statistics]),200
    else:
        return jsonify([{"message": "Player Not Found"}]),404


# provides the list of scheduled games
def find_schedule(requested_calendar):
    prepared_schedule = {}
    match_object = {}
    match_object['match'] = None
    match_object['scheduledDate'] = None

    for number in range(0,20):
        match_object['match'] = requested_calendar['data'][number]['name']
        match_object['scheduledDate'] = requested_calendar['data'][number]['date']
        prepared_schedule['game'+str(number+1)] = match_object
        match_object = {}
    return jsonify([prepared_schedule])

# Provides the scores for a game by taking matchId as input
def find_score_by_matchId(matchId):
    score_card =requests.get('https://cricapi.com/api/cricketScore?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2&unique_id={}'.format(matchId))
    modified_score_card = score_card.json()
    updated_score_card = {}
    updated_score_card['team-1'] = modified_score_card['team-1'] if 'team-1' in modified_score_card.keys() else None
    updated_score_card['team-2'] = modified_score_card['team-2'] if 'team-2' in modified_score_card.keys() else None
    updated_score_card['score'] = modified_score_card['score'] if 'score' in modified_score_card.keys() else None
    return updated_score_card
# provides the scores for already completed games
def find_old_match_scores(requested_scores):
    prepared_scores = {}
    for number in range(0,5):
        prepared_scores['game'+str(number+1)] = find_score_by_matchId(requested_scores['data'][number]['unique_id'])
    return jsonify([prepared_scores])

def find_new_match_scorebyid(matchId):
    score_card = requests.get(
        'https://cricapi.com/api/cricketScore?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2&unique_id={}'.format(matchId))
    modified_score_card = score_card.json()
    return modified_score_card['score'] if 'score' in modified_score_card.keys() else None

# provides the scores for ongoing games
def find_new_match_scores(requested_scores):
    prepared_scores = {}
    match_data = {}
    for number in range(0,10):
        score = find_new_match_scorebyid(requested_scores['matches'][number]['unique_id'])

        match_data['team-1'] = requested_scores['matches'][number]['team-1'] \
            if 'team-1' in requested_scores['matches'][number] else None

        match_data['team-2'] = requested_scores['matches'][number]['team-2'] \
            if 'team-2' in requested_scores['matches'][number] else None

        match_data['type'] = requested_scores['matches'][number]['type'] \
            if 'type' in requested_scores['matches'][number] else None

        match_data['toss_winner_team'] = requested_scores['matches'][number]['toss_winner_team'] \
            if 'toss_winner_team' in requested_scores['matches'][number] else None

        match_data['matchStarted'] = requested_scores['matches'][number]['matchStarted'] \
            if 'matchStarted' in requested_scores['matches'][number] else None

        match_data['score'] = score
        prepared_scores['game'+str(number+1)] = match_data
        match_data = {}
    return jsonify([prepared_scores])
