import re
from math import *

d_a = 79
text = r"""
\addplot [semithick, red!50!black]
table {%
25.9807621135332 225
25.9807621135332 255
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 165
259.807621135332 180
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 495
363.730669589464 510
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 390
337.749907475931 405
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 60
77.9422863405995 45
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 150
415.692193816531 120
};
\addplot [semithick, red!50!black]
table {%
207.846096908265 180
233.826859021798 195
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 300
181.865334794732 315
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 480
129.903810567666 465
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 270
389.711431702997 285
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 510
103.923048454133 480
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 435
51.9615242270663 450
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 -30
363.730669589464 0
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 450
415.692193816531 420
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 105
25.9807621135332 75
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 180
389.711431702997 195
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 270
129.903810567666 255
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 495
285.788383248865 525
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 165
467.653718043597 150
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 315
51.9615242270663 330
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 360
77.9422863405995 375
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 390
129.903810567666 405
};
\addplot [semithick, red!50!black]
table {%
0 480
0 510
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 375
467.653718043597 360
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 495
207.846096908265 510
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 435
337.749907475931 465
};
\addplot [semithick, red!50!black]
table {%
207.846096908265 60
181.865334794732 75
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 210
337.749907475931 225
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 465
51.9615242270663 480
};
\addplot [semithick, red!50!black]
table {%
519.615242270663 270
493.63448015713 285
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 105
259.807621135332 120
};
\addplot [semithick, red!50!black]
table {%
0 60
-25.9807621135332 45
};
\addplot [semithick, red!50!black]
table {%
389.711431702997 135
363.730669589464 120
};
\addplot [semithick, red!50!black]
table {%
311.769145362398 390
311.769145362398 360
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 480
389.711431702997 495
};
\addplot [semithick, red!50!black]
table {%
0 180
25.9807621135332 165
};
\addplot [semithick, red!50!black]
table {%
0 390
-25.9807621135332 375
};
\addplot [semithick, red!50!black]
table {%
129.903810567666 195
129.903810567666 165
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 75
467.653718043597 60
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 345
25.9807621135332 375
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 465
467.653718043597 480
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 300
77.9422863405995 285
};
\addplot [semithick, red!50!black]
table {%
389.711431702997 255
415.692193816531 270
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 240
337.749907475931 255
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 390
25.9807621135332 405
};
\addplot [semithick, red!50!black]
table {%
233.826859021798 15
233.826859021798 45
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 180
441.672955930064 195
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 45
337.749907475931 75
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 495
467.653718043597 510
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 15
103.923048454133 30
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 60
389.711431702997 45
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 150
129.903810567666 135
};
\addplot [semithick, red!50!black]
table {%
519.615242270663 120
493.63448015713 105
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 195
311.769145362398 180
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 420
129.903810567666 435
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 420
259.807621135332 390
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 0
285.788383248865 -15
};
\addplot [semithick, red!50!black]
table {%
0 0
25.9807621135332 15
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 225
77.9422863405995 195
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 15
519.615242270663 0
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 165
363.730669589464 150
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 180
51.9615242270663 150
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 135
519.615242270663 150
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 345
103.923048454133 330
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 450
233.826859021798 465
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 345
467.653718043597 330
};
\addplot [semithick, red!50!black]
table {%
0 300
-25.9807621135332 315
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 105
207.846096908265 90
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 240
51.9615242270663 210
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 405
207.846096908265 390
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 45
181.865334794732 15
};
\addplot [semithick, red!50!black]
table {%
233.826859021798 315
259.807621135332 300
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 240
129.903810567666 225
};
\addplot [semithick, red!50!black]
table {%
311.769145362398 240
285.788383248865 225
};
\addplot [semithick, red!50!black]
table {%
389.711431702997 75
389.711431702997 105
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 435
311.769145362398 450
};
\addplot [semithick, red!50!black]
table {%
0 420
0 450
};
\addplot [semithick, red!50!black]
table {%
129.903810567666 45
103.923048454133 60
};
\addplot [semithick, red!50!black]
table {%
129.903810567666 15
155.884572681199 30
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 390
129.903810567666 375
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 420
103.923048454133 450
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 375
493.63448015713 345
};
\addplot [semithick, red!50!black]
table {%
233.826859021798 165
207.846096908265 150
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 0
441.672955930064 15
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 45
0 30
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 270
181.865334794732 255
};
\addplot [semithick, red!50!black]
table {%
233.826859021798 435
233.826859021798 405
};
\addplot [semithick, red!50!black]
table {%
129.903810567666 285
129.903810567666 315
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 210
181.865334794732 195
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 195
0 210
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 405
311.769145362398 420
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 225
155.884572681199 240
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 285
311.769145362398 300
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 315
519.615242270663 330
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 90
441.672955930064 105
};
\addplot [semithick, red!50!black]
table {%
207.846096908265 480
233.826859021798 495
};
\addplot [semithick, red!50!black]
table {%
519.615242270663 450
493.63448015713 435
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 465
77.9422863405995 495
};
\addplot [semithick, red!50!black]
table {%
207.846096908265 330
207.846096908265 300
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 315
0 330
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 345
207.846096908265 360
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 30
415.692193816531 0
};
\addplot [semithick, red!50!black]
table {%
233.826859021798 285
207.846096908265 270
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 30
441.672955930064 45
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 300
441.672955930064 315
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 420
77.9422863405995 435
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 330
415.692193816531 300
};
\addplot [semithick, red!50!black]
table {%
25.9807621135332 495
25.9807621135332 525
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 0
181.865334794732 -15
};
\addplot [semithick, red!50!black]
table {%
0 150
25.9807621135332 135
};
\addplot [semithick, red!50!black]
table {%
389.711431702997 345
389.711431702997 375
};
\addplot [semithick, red!50!black]
table {%
129.903810567666 75
155.884572681199 60
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 210
441.672955930064 225
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 180
181.865334794732 165
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 75
259.807621135332 90
};
\addplot [semithick, red!50!black]
table {%
207.846096908265 30
207.846096908265 0
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 255
467.653718043597 270
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 90
415.692193816531 60
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 360
415.692193816531 390
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 120
441.672955930064 135
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 345
259.807621135332 330
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 165
103.923048454133 180
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 480
259.807621135332 510
};
\addplot [semithick, red!50!black]
table {%
519.615242270663 90
493.63448015713 75
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 285
155.884572681199 330
};
\addplot [semithick, red!50!black]
table {%
0 240
0 270
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 405
467.653718043597 420
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 135
207.846096908265 120
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 465
181.865334794732 435
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 210
233.826859021798 225
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 135
311.769145362398 150
};
\addplot [semithick, red!50!black]
table {%
233.826859021798 135
233.826859021798 105
};
\addplot [semithick, red!50!black]
table {%
207.846096908265 420
207.846096908265 450
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 120
77.9422863405995 105
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 360
129.903810567666 345
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 30
285.788383248865 45
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 0
51.9615242270663 30
};
\addplot [semithick, red!50!black]
table {%
0 90
-25.9807621135332 75
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 465
311.769145362398 480
};
\addplot [semithick, red!50!black]
table {%
389.711431702997 315
363.730669589464 330
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 345
311.769145362398 330
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 315
285.788383248865 285
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 300
337.749907475931 315
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 420
389.711431702997 435
};
\addplot [semithick, red!50!black]
table {%
311.769145362398 120
337.749907475931 105
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 480
389.711431702997 465
};
\addplot [semithick, red!50!black]
table {%
493.63448015713 495
493.63448015713 465
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 450
389.711431702997 405
};
\addplot [semithick, red!50!black]
table {%
103.923048454133 0
103.923048454133 -30
};
\addplot [semithick, red!50!black]
table {%
415.692193816531 240
415.692193816531 210
};
\addplot [semithick, red!50!black]
table {%
311.769145362398 90
311.769145362398 60
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 30
389.711431702997 15
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 135
103.923048454133 150
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 90
155.884572681199 120
};
\addplot [semithick, red!50!black]
table {%
181.865334794732 375
155.884572681199 360
};
\addplot [semithick, red!50!black]
table {%
129.903810567666 105
103.923048454133 90
};
\addplot [semithick, red!50!black]
table {%
0 360
-77.9422863405995 345
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 270
233.826859021798 255
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 120
51.9615242270663 90
};
\addplot [semithick, red!50!black]
table {%
519.615242270663 30
493.63448015713 45
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 60
233.826859021798 75
};
\addplot [semithick, red!50!black]
table {%
311.769145362398 0
311.769145362398 30
};
\addplot [semithick, red!50!black]
table {%
207.846096908265 210
207.846096908265 240
};
\addplot [semithick, red!50!black]
table {%
-25.9807621135332 105
0 120
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 435
467.653718043597 450
};
\addplot [semithick, red!50!black]
table {%
77.9422863405995 255
51.9615242270663 270
};
\addplot [semithick, red!50!black]
table {%
51.9615242270663 300
25.9807621135332 285
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 -15
337.749907475931 15
};
\addplot [semithick, red!50!black]
table {%
259.807621135332 240
285.788383248865 255
};
\addplot [semithick, red!50!black]
table {%
337.749907475931 375
363.730669589464 360
};
\addplot [semithick, red!50!black]
table {%
389.711431702997 225
415.692193816531 180
};
\addplot [semithick, red!50!black]
table {%
233.826859021798 345
259.807621135332 360
};
\addplot [semithick, red!50!black]
table {%
311.769145362398 210
285.788383248865 195
};
\addplot [semithick, red!50!black]
table {%
155.884572681199 450
129.903810567666 495
};
\addplot [semithick, red!50!black]
table {%
363.730669589464 90
389.711431702997 165
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 135
259.807621135332 150
};
\addplot [semithick, red!50!black]
table {%
285.788383248865 375
233.826859021798 375
};
\addplot [semithick, red!50!black]
table {%
519.615242270663 180
493.63448015713 195
};
\addplot [semithick, red!50!black]
table {%
467.653718043597 240
441.672955930064 255
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 165
493.63448015713 225
};
\addplot [semithick, red!50!black]
table {%
441.672955930064 405
467.653718043597 390
};
"""


a = re.compile(r"""\\addplot \[semithick, red.*\]
table \{%
(?P<x1>\d+\.\d+) (?P<y1>\d+(\.\d+)?)
(?P<x2>\d+\.\d+) (?P<y2>\d+(\.\d+)?)
\};""")

matches = a.finditer(text)

for match in matches:
    x1 = match.group("x1")
    x2 = match.group("x2")
    y1 = match.group("y1")
    y2 = match.group("y2")
    if sqrt((float(x1)-float(x2))**2+(float(y1)-float(y2))**2) >= d_a:
        print("{} {}".format(x1, y1))
        print("{} {}".format(x2, y2))

