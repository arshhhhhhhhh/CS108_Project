#!/bin/bash

sortf="${1}"
echo "$sortf"
if [ ! -f "history.csv" ]; then
    echo "Error: history.csv not found"
    return 1
fi

declare -A a_wn a_ls a_ps a_gm

while IFS=',' read -r winner loser date game; do
    a_wn["$game;$winner"]=$(( ${a_wn["$game;$winner"]:-0} + 1 ))
    a_ls["$game;$loser"]=$(( ${a_ls["$game;$loser"]:-0} + 1 ))
    a_ps["$game;$winner"]=1
    a_ps["$game;$loser"]=1
    a_gm["$game"]=1
done < history.csv

for game in "${!a_gm[@]}"; do
    echo "Game: $game"
    echo "PLAYER, WINS, LOSSES, WIN/LOSS RATIO"
    lines=""
    for key in "${!a_ps[@]}"; do
        if [[ $(echo $key | sed 's/;.*//') == $game ]]; then
            ps_i=${key#"$game;"}
            w_i=${a_wn["$key"]:-0}
            l_i=${a_ls["$key"]:-0}
            rto_i="0.00"
            if [ $l_i -gt 0 ]; then
                rto_i=$(echo "scale=2; $w_i / $l_i" | bc)
            else
                rto_i="INF"
            fi
            if [[ "$sortf" == "0" ]]; then
                lines+=$(printf "%d %s %d %.2f\n" "$w_i" "$ps_i" "$l_i" "$rto_i")
            elif [[ "$sortf" == "1" ]]; then
                lines+=$(printf "%d %.2f %s %d\n" "$l_i" "$rto_i" "$ps_i" "$w_i")
            else
                lines+=$(printf "%.2f %s %d %d\n" "$rto_i" "$ps_i" "$w_i" "$l_i")
            fi
            lines+=$'\n'
        fi
    done
    lines="${lines::-1}"

    # Sort and format output
    if [ -n "$lines" ]; then
        echo "$lines" | sort -r | awk '
        {
            if ("'$sortf'" == "0") {
                print $2 "," $1 "," $3 "," $4 
            } else if ("'$sortf'" == "1") {
                print $3 "," $4 "," $1 "," $2 
            } else {
                print $2 "," $3 "," $4 "," $1 
            }
        }
        ' | column -t -s','
    else
        echo "No data for this game"
    fi
    echo ""
done
