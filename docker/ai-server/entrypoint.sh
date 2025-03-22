#!/bin/bash

cd /opt/toontown/src

IFS=$'\n'
districtNames=(
    "Boingy Acres" "Boingy Bay" "Boingy Summit" "Boingyboro" "Bouncy Summit"
    "Crazy Grove" "Crazy Hills" "Crazyham" "Funnyfield" "Giggly Bay" "Giggly Grove"
    "Giggly Hills" "Giggly Point" "Gigglyfield" "Gigglyham" "Goofy Valley"
    "Goofyport" "Kooky Grove" "Kookyboro" "Loopy Harbor" "Nutty Hills" "Nutty River"
    "Nutty Summit" "Nuttyville" "Nuttywood" "Silly Rapids" "Silly Valley" "Sillyham"
    "Toon Valley" "Zany Acres"
)
declare -a PIDS=()

shuffle() {
    local i tmp size max rand
    size=${#districtNames[*]}
    max=$(( size - 1 ))
    for ((i = 0; i < max; i++)); do
        rand=$(( RANDOM % (max - i) + i ))
        tmp=${districtNames[i]}
        districtNames[i]=${districtNames[rand]}
        districtNames[rand]=$tmp
    done
}

shuffle
cutDistrictNames=("${districtNames[@]:0:$NUM_DISTRICTS}")

start_district() {
    python3 -m toontown.ai.AIStart --base-channel $AI_BASE_CHANNEL \
                                   --max-channels $MAX_CHANNELS --stateserver $STATE_SERVER \
                                   --messagedirector-ip $MESSAGE_DIRECTOR_IP \
                                   --eventlogger-ip $EVENT_LOGGER_IP --district-name "$DISTRICT_NAME" &

    PIDS+=($!)
    echo "District $districtName started with BASE_CHANNEL $AI_BASE_CHANNEL"
}

for districtName in "${cutDistrictNames[@]}"; do
    export DISTRICT_NAME="$districtName"
    export AI_BASE_CHANNEL=$((AI_BASE_CHANNEL + 1000000))
    start_district "$districtName"
    sleep 5
done

echo "All districts started"
for pid in "${PIDS[@]}"; do
    wait $pid
done