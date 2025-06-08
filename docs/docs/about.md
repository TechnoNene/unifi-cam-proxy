---
slug: /
sidebar_position: 1
---

**unifi-cam-proxy** adds UniFi Protect compatibility to non-UniFi cameras. It goes beyond the basic third-party camera functionality of UniFi Protect for ONVIF Cameras added by Ubiquiti. Key features include:

**unifi-cam-proxy** extends UniFi Protect to work with non-UniFi cameras, enabling enhanced compatibility and advanced features not natively supported by Ubiquiti, when using ONVIF.

Unlike the basic ONVIF support recently introduced by UniFi Protect, this tool offers a more flexible and powerful solution. Key features include:


- **Ubiquiti Camera Emulation:** Simulates a UniFi camera to integrate seamlessly with Protect.
- **Motion Detection:** Supports event-based recording to save storage and bandwidth.
- **Smart Detections:** Enables recording based on object detection, such as people or vehicles.
- **Camera-Specific Tweaks:** Includes custom support for certain models (e.g., Hikvision).
- **RTSP Compatibility:** Works with any RTSP camera, even those lacking ONVIF support.
- **Multiple instance support?** Allows multiple cameras from a single DVR/NVR source to be added independently to Protect — useful since ONVIF support typically limits to one camera per ONVIF device.

This project is a fork of [Keshav Varma](https://github.com/keshavdv/unifi-cam-proxy)'s original implementation and has been extended and maintained to add more features and improvements.

## Credits and Thanks

This version is a continuation of a work originally created by [Keshav Varma](https://github.com/keshavdv/unifi-cam-proxy), and has evolved through the valuable contributions and forks of:

- [Allram](https://github.com/Allram/unifi-cam-proxy) *(this fork was created from here)*
- [zacharee](https://github.com/zacharee/unifi-cam-proxy)
- [JasonGehring](https://github.com/JasonGehring/unifi-cam-proxy)

Each has contributed enhancements and improvements along the way. This fork aims to build upon that foundation with further development, documentation, and features.
