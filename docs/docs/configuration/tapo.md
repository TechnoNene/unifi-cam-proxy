---
sidebar_position: 1
---

# Tapo

Unifi-cam-proxy has basic support for Tapo/TPlink cameras, like the C100 or C200 with PTZ.

To control the PTZ functionality, use the camera image settings in UniFi.
Adjust the contrast below 20 to pan left and above 80 to pan right.
The brightness setting controls the tilt.
Reset brightness and contrast to around 50 after adjusting the camera position.
Otherwise you may change the position by accident.

## Standard

```sh
unifi-cam-proxy -H {NVR IP} -i {Camera IP} -c /client.pem -t {Adoption token} --mac 'AA:BB:CC:00:11:22'\
  tapo \
  --rtsp "rtsp://{camera_username}:{camera_password}@{camera_ip}:554"
```

### H.265 Example

```sh
unifi-cam-proxy -H {NVR IP} -i {Camera IP} -c /client.pem -t {Adoption token} --mac 'AA:BB:CC:00:11:22'\
  tapo \
  --rtsp "rtsp://{camera_username}:{camera_password}@{camera_ip}:554" \
  --video-codec h265
```

## PTZ Support

```sh
unifi-cam-proxy -H {NVR IP} -i {Camera IP} -c /client.pem -t {Adoption token} --mac 'AA:BB:CC:00:11:22'\
  tapo \
  --rtsp "rtsp://{camera_username}:{camera_password}@{camera_ip}:554"\
  --password "{TP Link account Password}"
```
