# V2.1: increased efficiency

directions = ((0,1),(1,0),(0,-1),(-1,0))
MAXDEPTH = 8

def getTileScores(data):
  tileScores = {}
  board = data["board"]
  height = board["height"]
  width = board["width"]
  snakes = board["snakes"]
  food = board["food"]
  mySnake = data["you"]
  myLength = mySnake["length"]
  myID = mySnake["id"]
  for tile in food:
    tileScores[(tile["x"], tile["y"])] = 150
  for snake in snakes:
    if snake["id"] != myID:
      head = snake["head"]
      for direction in directions:
        newHead = (head["x"] + direction[0], head["y"] + direction[1])
        if myLength > snake["length"]:
          tileScores[newHead] = 300
        else:
          tileScores[newHead] = 25
    for tile in snake["body"]:
      tileScores[(tile["x"], tile["y"])] = 0
  for x in range(width):
    for y in range(height):
      coord = (x, y)
      if coord not in tileScores:
        tileScores[coord] = 100
  return tileScores

def findBestMove(coord, tileScores, width, height, myLength):

  def findBestPathRec(coord, depth, simTiles):
    depth += 1
    x, y = coord
    if x < 0 or y < 0 or x >= width or y >= height:
      return 0
    if coord in simTiles:
      return 0
    score = tileScores[coord]
    if score == 0:
      return 0
    if depth > MAXDEPTH:
      return score
    nextTileScores = []
    for direction in directions:
      nextTileScores.append(findBestPathRec((x + direction[0], y + direction[1]), depth, simTiles.union({coord})))
    best = score + max(nextTileScores)
    return best
  
  x, y = coord
  moveDirs = {"up":(x, y + 1),"right":(x + 1, y),"down":(x, y - 1),"left":(x - 1, y)}
  moves = {"up":0,"right":0,"down":0,"left":0}
  for move in moves:
    newCoord = moveDirs[move]
    moves[move] = findBestPathRec(newCoord, 0, set())
  return max(moves, key = moves.get)

def chooseMove(data):
  board = data["board"]
  mySnake = data["you"]
  height = board["height"]
  width = board["width"]
  x = mySnake["head"]["x"]
  y = mySnake["head"]["y"]
  myLength = mySnake["length"]
  tileScores = getTileScores(data)
  return findBestMove((x, y), tileScores, width, height, myLength)
