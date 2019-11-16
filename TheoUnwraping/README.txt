

STILL NEED DEBBUGING !!

_______________________________________
COMMANDS:

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
