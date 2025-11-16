
import math

YELLOW = [0.587, 0.357, 0.054]
ORANGE = [0.735, 0.218, 0.044]
L_BLUE = [0.326, 0.320, 0.353]
W_B = [0.422, 0.306, 0.264]
GREEN = [0.462, 0.462, 0.070]
RED = [0.910, 0.050, 0.035]

def classify_it(r_avg, g_avg, b_avg, intensity):
    y = math.sqrt(math.pow((YELLOW[0]-r_avg/intensity), 2)+math.pow((YELLOW[1]-g_avg/intensity), 2)+math.pow((YELLOW[2]-b_avg/intensity), 2))
    o = math.sqrt(math.pow((ORANGE[0]-r_avg/intensity), 2)+math.pow((ORANGE[1]-g_avg/intensity), 2)+math.pow((ORANGE[2]-(b_avg/intensity)), 2))
    b = math.sqrt(math.pow((L_BLUE[0]-r_avg/intensity), 2)+math.pow((L_BLUE[1]-g_avg/intensity), 2)+math.pow((L_BLUE[2]-b_avg/intensity), 2))
    WB = math.sqrt(math.pow((W_B[0]-r_avg/intensity), 2)+math.pow((W_B[1]-g_avg/intensity), 2)+math.pow((W_B[2]-b_avg/intensity), 2))
    g = math.sqrt(math.pow((GREEN[0]-r_avg/intensity), 2)+math.pow((GREEN[1]-g_avg/intensity), 2)+math.pow((GREEN[2]-b_avg/intensity), 2))
    r = math.sqrt(math.pow((RED[0]-r_avg/intensity), 2)+math.pow((RED[1]-g_avg/intensity), 2)+math.pow((RED[2]-b_avg/intensity), 2))
    print("y: ", y, "o: ", o, "b: ", b, "WB: ", WB)

    if (y < o and y < b and y < WB and y < g and y < r):
        return "yellow"
    elif (o < y and o < b and o < WB and o < g and o < r):
        return "orange"
    elif (b < y and b < o and b < WB and b < g and b < r):
        return "blue"
    elif (g < y and g < o and g < b and g < WB and g < r):
        return "green"
    elif (r < y and r < o and r < b and r < WB and r < g):
        return "red"
    elif (intensity < 100):
        return "black"
    else:
        return "white"




