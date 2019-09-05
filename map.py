n = int(input('Enter the number: '))

boxes = [[0]*x for x in range(1, n+2)]
boxes[0][0]  = 1
count = 0
for x in range(1,n+1):
    for y in range(x+1):
        if(y >= 0):
            boxes[x][y] = boxes[x][y] + boxes[x][y-1]
        if(x-1>=0 and y < len(boxes[x-1])):
            boxes[x][y] = boxes[x][y] + boxes[x-1][y]
        if(x>0 and y>0):
            boxes[x][y] = boxes[x][y] + boxes[x-1][y-1]

print boxes[n][n]
