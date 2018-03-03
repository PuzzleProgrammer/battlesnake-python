import bottle
import os
import random

#2018

def populateGrid(grid):
    return

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
    headPos = {'x':data.you.body.data[0]["x"], 'y':data.you.body.data[0]["y"]}
    grid = [board_width][board_height]
    populateGrid(grid);
    directions = ['up', 'down', 'left', 'right']
    
    if (headPos['x'] == 0 or grid[headPos['x']-1,headPos['y']] != 0):
        directions.remove('left')
    if (headPos['x'] == board_width-1 or grid[headPos['x']+1,headPos['y']] != 0):
        directions.remove('right')
    if (headPos['y'] == 0 or grid[headPos['x'],headPos['y']-1] != 0):
        directions.remove('up')
    if (headPos['y'] == board_height-1 or grid[headPos['x'],headPos['y']+1] != 0):
        directions.remove('down')
    
    direction = random.choice(directions)
    print(directions)
    return {
        'move': direction,
        'taunt': "{}".format(directions)
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
