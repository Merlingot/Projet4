
******* ICI ********
_______________________________________
COMMANDS for functionning unwrapping:

#############################
##-Get les photos des patterns projetté
1) Projettez les photos du folder "fringes" sur l'écran
2) Prendre photo avec la camera AV et placer la photo dans le folder scan_AV avec le nom "dstFringes_XXX.png" où XXX est le numéro correspondant au nom de la photo de fringe projetté
3) Fait la même chose avec la point grey dans le folder scan_PG

4) faire les commandes
		cl3ds_match -m phaseshift_matcher_AV.xml -k "cam match" -o cam_match_AV.png
		cl3ds_match -m phaseshift_matcher_PG.xml -k "cam match" -o cam_match_PG.png

5) Voila (si ca marche pas dites moi le
