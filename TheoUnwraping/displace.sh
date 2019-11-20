

cd PythonScripts

python3 warpWithDisplacement.py

cd ..

cl3ds_match -m phaseshift_matcher.xml -k "cam match" -o cam_match.png

cd PythonScripts

python3 seperateXY.py

cd ..


