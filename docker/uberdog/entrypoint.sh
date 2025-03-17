#!/bin/bash

cd /opt/toontown/src

python3 -m toontown.uberdog.UDStart \
    --base-channel ${UD_BASE_CHANNEL} \
    --max-channels ${MAX_CHANNELS} \
    --stateserver ${STATE_SERVER} \
    --messagedirector-ip ${MESSAGE_DIRECTOR_IP} \
    --eventlogger-ip ${EVENT_LOGGER_IP} \
    --auth-method ${AUTH_METHOD}