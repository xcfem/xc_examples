#!/bin/sh
# 
#   Copyright (C)  Luis C. Pérez Tato
# 
#   XC utils is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or 
#   (at your option) any later version.
# 
#   This software is distributed in the hope that it will be useful, but 
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.  
# 
#  You should have received a copy of the GNU General Public License 
#  along with this program.
#  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------

ERT="\\033[1;32m"
NORMAL="\\033[0;39m"
ROUGE="\\033[1;31m"
ROSE="\\033[1;35m"
BLEU="\\033[1;34m"
BLANC="\\033[0;02m"
BLANCLAIR="\\033[1;08m"
JAUNE="\\033[1;33m"
CYAN="\\033[1;36m"

echo ""

mplbackend_backup="nil"
# Trying to avoid Matplotlib complaining about the XServer
if [ -n "$MPLBACKEND" ]; then
    echo "$JAUNE" "MPLBACKEND already set as: $MPLBACKEND" "$NORMAL"
    mplbackend_backup="$MPLBACKEND"
else
    echo "$BLEU" "Setting MPLBACKEND to avoid Matplotlib complaints." "$NORMAL"
    MPLBACKEND=Agg
    export MPLBACKEND
fi

START=$(date +%s.%N)

# Misc. tests
echo "$BLEU" "Steel connections examples." "$NORMAL"
python steel_structure/connections/bolted_flange_plate_connection_predim.py silent
python steel_structure/connections/bolted_shear_tab_connection_predim.py silent

echo "$BLEU" "Reinforced concrete examples." "$NORMAL"
python ./reinforced_concrete/normal_stresses/ec2_bending_example.py silent
python ./reinforced_concrete/anchorage_length/ec2_anchorage_lenght.py silent




END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo $DIFF seconds
NT=$(grep -c '^python' $0)
echo ${NT} tests
Q=$(echo "$DIFF / $NT" | bc -l)
echo $Q seconds/test

# Restore MPLBACKEND to its previous value.
mplbackend_backup="nil"
# Trying to avoid Matplotlib complaining about the XServer
if [ "$mplbackend_backup"=="nil" ]; then
    echo "$BLEU" "Removing MPLBACKEND from environment variables" "$NORMAL"
    MPLBACKEND=''
else
   echo "$BLEU" "Restoring MPLBACKEND to its previous value." "$NORMAL"
   MPLBACKEND=mplbackend_backup
fi
export MPLBACKEND

# Clean garbage if any

rm -f -r ./annex
rm -f -r ./tmp
