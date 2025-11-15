
import math

YELLOW = [0.587, 0.357, 0.054]
ORANGE = [0.735, 0.218, 0.044]
L_BLUE = [0.326, 0.320, 0.353]
W_B = [0.422, 0.306, 0.264]

def classify_it(r_avg, g_avg, b_avg, intensity):
    y = math.sqrt(math.pow((YELLOW[0]-r_avg/intensity), 2)+math.pow((YELLOW[1]-g_avg/intensity), 2)+math.pow((YELLOW[2]-b_avg/intensity), 2))
    o = math.sqrt(math.pow((ORANGE[0]-r_avg/intensity), 2)+math.pow((ORANGE[1]-g_avg/intensity), 2)+math.pow((ORANGE[2]-(b_avg/intensity)), 2))
    b = math.sqrt(math.pow((L_BLUE[0]-r_avg/intensity), 2)+math.pow((L_BLUE[1]-g_avg/intensity), 2)+math.pow((L_BLUE[2]-b_avg/intensity), 2))
    WB = math.sqrt(math.pow((W_B[0]-r_avg/intensity), 2)+math.pow((W_B[1]-g_avg/intensity), 2)+math.pow((W_B[2]-b_avg/intensity), 2))
    print("y: ", y, "o: ", o, "b: ", b, "WB: ", WB)

    if (y < o and y < b and y < WB):
        return "yellow"
    elif (o < y and o < b and o < WB):
        return "orange"
    elif (b < y and b < o and b < WB):
        return "blue"
    elif (intensity < 200):
        return "black"
    else:
        return "white"




