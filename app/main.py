import bottle
import os
import random

#2018

def gridPop(data):
    grid = [[0 for x in range(data['height'])] for x in range(data['width'])]
    for snakes in data['snakes']['data']:
        for body in snakes['body']['data']:
            grid[body['x']][body['y']] = 1
    return grid


def goToTarget(mySnake, x, y, validDirs):
    xDist = mySnake['body']['data'][0]['x'] - x
    yDist = mySnake['body']['data'][0]['y'] - y

    desiredDirs = []

    if xDist > 0 and "left" in validDirs:
        desiredDirs.append("left")
    elif xDist < 0 and "right" in validDirs:
        desiredDirs.append("right")

    if yDist > 0 and "up" in validDirs:
        desiredDirs.append("up")
    elif yDist < 0 and "down" in validDirs:
        desiredDirs.append("down")

    if len(desiredDirs) == 0:
        return validDirs

    return desiredDirs

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

    head_url = '%s://%s/static/download.jpg' % (
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
    # top left is 0,0
    headPos = {'x':data['you']['body']['data'][0]["x"], 'y':data['you']['body']['data'][0]["y"]}
    grid = gridPop(data)
    directions = ['up', 'down', 'left', 'right']
    
    if (headPos['x'] == 0 or grid[headPos['x']-1][headPos['y']] != 0):
        directions.remove('left')
    if (headPos['x'] == data['width']-1 or grid[headPos['x']+1][headPos['y']] != 0):
        directions.remove('right')
    if (headPos['y'] == 0 or grid[headPos['x']][headPos['y']-1] != 0):
        directions.remove('up')
    if (headPos['y'] == data['height']-1 or grid[headPos['x']][headPos['y']+1] != 0):
        directions.remove('down')
        
    xPos=data['you']['body']['data'][-1]["x"]
    yPos=data['you']['body']['data'][-1]["y"]
    if data['you']['health'] < 50:
        xPos = data['food']['data'][0]['x']
        yPos = data['food']['data'][0]['y']
    
    directions = goToTarget(data['you'],xPos,yPos,directions)
    
    direction = random.choice(directions)
   # print("" + headPose[0] + ", " + headPose[1])
    return {
        'move': direction,
        'taunt': 'AAAAAAAAAAAAAAAGHH!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
