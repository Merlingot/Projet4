

_______________________________________
##-Distortion parameters:

 k1 = ; #-Barrel (Positive) or Pincushion (Negative) Distortion (~1e-3)
 k2 = ; #-Mustache distortion ?? (~1e-7)
 p1 = ; #-Angle of view (Vertical) (~1e-3)
 p2 = ; #-Angle of view (Horizontal) (~1e-3)
 k3 = ; #-??
 k4 = ; #-??
 k5 = ; #-Borders ??
 k6 = ; #-??

#-For Displacement, set offset in function


_______________________________________
COMMANDS for functionning unwrapping:

###########################
##-Distort Fringes with arbitrary function :
#-Parameters can be changed in the python functions (see above comments)

(Perfect Setup)
python3 warpNoDisplacement.py

(Imperfect Setup)
python3 wardWithDisplacement.py

#############################
##-Get mapping

cl3ds_match -m phaseshift_matcher.xml -k "cam match" -o cam_match.png


_______________________________________
COMMANDS for full unwrapping:
(Still causes segmentation fault!)

###########################
#-Create config (Default) :

cl3ds_create_generator_config -d -m phaseshift -o phaseshift.xml

###########################
#-Generate Patterns :

cl3ds_generate -g phaseshift.xml -o fringes/fringes_%03d.png -f -1

###########################
#-Distort Fringes :

(Perfect Setup)
python3 warpNoDisplacement.py

(Imperfect Setup)
python3 wardWithDisplacement.py

###########################
#-Create Matcher :

echo y phaseshift.xml generator allFrequencies thScan/dstFringes_%03d.png 31 0 1 | cl3ds_create_matcher_config -m phaseshift -c seqreader -p dummy

###########################
#-Unwraping

cl3ds_match -m phaseshift_matcher.xml -k "cam match" -o cam_match.png



