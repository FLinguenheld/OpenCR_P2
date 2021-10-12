#! env/bin/python3
""" Terminal progress bar """

from math import floor

counter = 0
def showProgressBar(progression):
    """ Display a progress bar in the terminal with the given list
        Optional text after the bar
        [XXXX\––––] -- text1 text2

        Arguments :
            progression (list) :   (total, done, text1, text2...)
    """

    global counter
    l = ["|", "/", "–", "\\", "|", "/", "–", "\\"]


    if progression[0] > 0:

        counter += 1
        if counter >= 8:
            counter = 0

        p = str()
        for i in range(progression[1]):
            p += "X"

        if progression[1] < progression[0]:
            p += l[counter]

            for i in range(progression[0] - progression[1] -1):
                p += "–"

        txt = str()
        for i in range(2,len(progression)):
            txt += progression[i]


        print(f"\033[K[{p}] {txt}", end="\r")        # \033[K : erase the current text


# --
if __name__ == "__main__":
    print("Test progressBar")
    progression = [10, 0, ""]
    for i in range(0, 100000001):
        
        if i % 100000 == 0:
            progression[1] = floor(i * 10 / 100000000)
            progression[2] = str(i)
            showProgressBar(progression)

