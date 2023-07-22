#!/bin/bash
PID=$$
git clone --no-checkout --depth 1 git@github.com:judge-meister/keys.git tmp${PID} >/dev/null 2>&1 && cd tmp${PID} && echo "let openweatherapi = '$(git show HEAD:api/openweather.key)';" > ../config.js && cd - >/dev/null && rm -rf tmp${PID}


