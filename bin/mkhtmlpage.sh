#!/bin/bash
# shellcheck disable=SC2162

function mkpage()
{
cat > index.html << .EOF
<html>
<head>
<style>
img { border: 1px solid #444444 }
a { color: #cccccc; text-decoration: none }
a:hover { color: #777777; }
.folders { margin-bottom: 10px }
</style>
</head>
<div class="folders">
.EOF
(
echo "<body bgcolor=\"#222222\">"
echo "<a href=\"..\"><b>[</b> up <b>]</b></a> "
find . -maxdepth 1 -mindepth 1 -type l -o -type d | sort | while read x; 
do 
  if [ -d "$(realpath "$x")" ]
  then
    y=${x/\.\//}
    echo "<a href=\"$y\"><b>[</b> $y <b>]</b></a>"
  fi
done
echo "</div>"
find . -maxdepth 1 -name "*.jp*g" -o -name "*.png" | sort | while read x;
do 
  if [ -f "$x" ] || [ -h "$x" ]
  then 
    echo "<a href=\"$x\"><img src=\"$x\" height=240/></a>"
  fi
done
echo "</body>" 
) >> index.html
echo "</html>" >> index.html
}

CWD=$(pwd)
find -L . -type d -o -type l | while read x
do 
  cd "${x/\.\//}" || exit
  echo "$x"
  mkpage
  cd "$CWD" || exit
done
