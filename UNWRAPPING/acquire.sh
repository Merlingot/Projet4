# -------------------------------------------- #
#         Data acquisition script              #
# -------------------------------------------- #

# --------------------------------------------------------------- #
# This bash script acquires the distorted fringes from original   #
# fringes in order to make surface cartography with codedlight    #
# library                                                         #
#                                                                 #
# Usage:           bash acquire.sh {make_arg}                     #
# --------------------------------------------------------------- #

## Function definition

save_Thrash(){
	cd archive
	local found = false
	local i=$0

	while["$found"=false];
	do
		if [ ! -d "scan_$ ]

}

# Check if build/ dir exists.
if [ ! -d scan_AV_3channels ]; then
	mkdir scan_AV_3channels
else
	cp -r scan_AV_3channels
	mkdir  scan_AV_3channels
fi

if [ ! -d scan_PG_3channels ]; then
	mkdir scan_PG_3channels
else
	rm -rf scan_PG_3channels
	mkdir scan_PG_3channels
fi



