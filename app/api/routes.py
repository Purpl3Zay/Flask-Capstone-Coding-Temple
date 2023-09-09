from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Team, team_schema, teams_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/teams', methods = ['POST'])
@token_required
def create_team(current_user_token):
    teamname = request.json['teamname']
    city = request.json['city']
    league = request.json['league']
    record = request.json['record']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    team = Team(teamname, city, league, record, user_token = user_token )

    db.session.add(team)
    db.session.commit()

    response = team_schema.dump(team)
    return jsonify(response)


@api.route('/teams', methods = ['GET'])
@token_required
def get_team(current_user_token):
    a_user = current_user_token.token
    teams = Team.query.filter_by(user_token = a_user).all()
    response = teams_schema.dump(teams)
    return jsonify(response)

@api.route('/teams/<id>', methods = ['GET'])
@token_required
def get_single_team(current_user_token, id):
    team = Team.query.get(id)
    response = team_schema.dump(team)
    return jsonify(response)

@api.route('/teams/<id>', methods = ['POST','PUT'])
@token_required
def update_team(current_user_token,id):
    team = Team.query.get(id) 
    team.teamname = request.json['teamname']
    team.city = request.json['city']
    team.league = request.json['league']
    team.record = request.json['record']
    team.user_token = current_user_token.token

    db.session.commit()
    response = team_schema.dump(team)
    return jsonify(response)

@api.route('/teams/<id>', methods = ['DELETE'])
@token_required
def delete_team(current_user_token, id):
    team = Team.query.get(id)
    db.session.delete(team)
    db.session.commit()
    response = team_schema.dump(team)
    return jsonify(response)
