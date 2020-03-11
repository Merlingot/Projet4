# ---------------------------------------- #
#         Cartographie script              #
# ---------------------------------------- #

# --------------------------------------------------------------- #
# This bash script simply calls a python script in order to fix   #
# png files from 3 channels to single channel in order to use     #
# th coded light library for phase unwrapping                     #
#                                                                 #
# Usage:           bash unwrap.sh {make_arg}                      #
# --------------------------------------------------------------- #

# Check if build/ dir exists.
if [ ! -d scan_AV ]; then
    mkdir scan_AV
else
    rm -rf scan_AV
    mkdir  scan_AV
fi

if [ ! -d scan_PG ]; then
    mkdir scan_PG
else
    rm -rf scan_PG
    mkdir scan_PG
fi

python3 channelFix.py

cl3ds_match -m phaseshift_matcher_AV.xml -k "cam match" -o cam_match_AV.png
cl3ds_match -m phaseshift_matcher_PG.xml -k "cam match" -o cam_match_PG.png

