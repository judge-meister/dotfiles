FROM debian:sid-slim
LABEL maintainer "Ian Judge <ianjudge@linux.com>"

RUN apt-get update && apt-get install -y \
	tigervnc-viewer \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["vncviewer" ]


#	&& rm -rf /var/lib/apt/lists/*
#	libgl1-mesa-dri \
#	libgl1-mesa-glx \
#   inetutils-ping \

