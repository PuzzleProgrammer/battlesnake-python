import bottle
import os
import random

#2018


@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    # TODO: Do things with data

    return {
        'color': '#FFFF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data
    
    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    print(direction)
    
    return {
        'move': direction,
        'taunt': 'battlesnake-python!'
    }

def goToTarget(mySnake, x, y, validDirs):
    xDist = mySnake.body.data[0].x - x
    yDist = mySnake.body.data[0].y - y

    desiredDirs = []

    if xDist > 0 and "left" in validDirs:
        desiredDirs += "left"
    elif xDist < 0 and "right" in validDirs:
        desiredDirs += "right"

    if yDist > 0 and "up" in validDirs:
        desiredDirs += "up"
    elif yDist < 0 and "down" in validDirs:
        desiredDirs += "down"

    if desiredDirs.count == 0:
        return validDirs

    return desiredDirs

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
