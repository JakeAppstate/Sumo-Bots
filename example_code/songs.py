from zumo_2040_robot import robot
import time
#imperial march, possibly
imperial = (
    "! O5 T100 L8 "
     "g g g "
      "d.16 <b- g "
       "d.16 <b- g "
        "d >d d "
      "<b- f e- d "
       "<b-"
)
buzzer.play_in_background(imperial)
