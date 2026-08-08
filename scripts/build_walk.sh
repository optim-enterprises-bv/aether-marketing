#!/usr/bin/env bash
# Assemble the captured Aether UI frames into a 1080x1080 walkthrough.
set -euo pipefail
S=/tmp/claude-1000/-home-dingo/8fa87e8a-7333-473f-918d-8297ebd71765/scratchpad
W=$S/walk
SEG=$S/segs
FONT=/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf
mkdir -p "$SEG"; rm -f "$SEG"/*.mp4

# scene: src  dur  zoom-target-x  zoom-target-y  caption1  caption2
scene () {
  local src=$1 dur=$2 zx=$3 zy=$4 c1=$5 c2=${6:-}
  local out="$SEG/$(basename "$src" .png)-$RANDOM.mp4"
  # crop 1600x1000 -> square-ish region, slow push-in, pad to 1080 square
  local vf="scale=1728:1080:force_original_aspect_ratio=increase,crop=1080:1080:${zx}:${zy}"
  vf="$vf,zoompan=z='min(1+0.00055*on,1.05)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1080:fps=30"
  vf="$vf,drawbox=y=ih-190:w=iw:h=190:color=0x0B0F14@0.86:t=fill"
  vf="$vf,drawtext=fontfile=${FONT}:text='${c1}':fontcolor=0xF0F4F8:fontsize=40:x=(w-text_w)/2:y=h-150"
  [ -n "$c2" ] && vf="$vf,drawtext=fontfile=${FONT}:text='${c2}':fontcolor=0x9CA3AF:fontsize=32:x=(w-text_w)/2:y=h-95"
  vf="$vf,format=yuv420p"
  ffmpeg -y -loglevel error -framerate 30 -loop 1 -t "$dur" -i "$src" -vf "$vf" -r 30 \
         -c:v libopenh264 -b:v 8M "$out"
  echo "file '$out'" >> "$SEG/list.txt"
}

: > "$SEG/list.txt"

scene "$W/dashboard.png"     8 324 0   "15 devices. 11 protocols. One pane." "Live topology, anomalies, traffic"
scene "$W/devices.png"       9 324 0   "uCentral · TR-369 · WRP · OpenSync · EasyMesh" "NETCONF · gNMI · SNMP · LwM2M · IoT MQTT · CoAP · STOMP"
scene "$W/devices.png"       6 560 380 "A real Banana Pi BPI-R4 on USP/TR-369" "alongside every protocol simulator"
scene "$W/topology.png"     10 324 0   "One topology. Every protocol." "Fixed, transport and IoT in one graph"
scene "$W/events.png"        5 324 0   "Live event stream"
scene "$W/pki.png"           5 324 0   "Post-quantum PKI" "X25519 + ML-KEM-768, certs per device"
scene "$W/tmf.png"           5 324 0   "TMF Open API" "TMF621 / 632 / 638 / 678"
scene "$W/billing.png"       5 324 0   "Billing and metering" "usage-based, per device"

ffmpeg -y -loglevel error -f concat -safe 0 -i "$SEG/list.txt" -c copy "$S/aether-walkthrough-raw.mp4"
ffmpeg -y -loglevel error -i "$S/aether-walkthrough-raw.mp4" \
  -vf "format=yuv420p" -r 30 -c:v libopenh264 -b:v 8M -movflags +faststart \
  "$S/aether-walkthrough.mp4"
ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,width,height -of default=nw=1 "$S/aether-walkthrough.mp4"
