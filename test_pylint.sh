#!/bin/bash
#
# this is a modified version of the same script from github.com/jessfraz/dotfiles
#
set -e
set -o pipefail

ERRORS=()

# find all executables and run `pylint`
for f in $(find . -type f -not -path '*.git*' -not -path '*/qtile/*' | sort -u); do
	if file "$f" | grep --quiet Python; then
		{
			pylint "$f" >/tmp/pylint.out && echo "[OK]: successfully pylinted $f"
		} || {
            cat /tmp/pylint.out
			# add to errors
			ERRORS+=("$f")
		}
	fi
done


if [ ${#ERRORS[@]} -eq 0 ]; then
	echo "No errors, hooray"
else
	echo -e "\nThese files failed pylint: ${ERRORS[*]}"
	exit 1
fi

