# UniFi Camera Proxy

## About

This enables using non-Ubiquiti cameras within the UniFi Protect ecosystem. This is
particularly useful to use existing RTSP-enabled cameras in the same UI and
mobile app as your other Unifi devices.

Things that work:

* Live streaming
* Full-time recording
* Motion detection with certain cameras
* Smart Detections using [Frigate](https://github.com/blakeblackshear/frigate)

## Documentation

View the documentation at <https://technonene.github.io/unifi-cam-proxy/>

Replace the `image: ...` line in `docker-compose.yml` with `build: https://github.com/technonene/unifi-cam-proxy.git`.
