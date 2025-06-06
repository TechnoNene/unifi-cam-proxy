import argparse
import logging
import tempfile
from pathlib import Path
from typing import Any

import httpx
from amcrest import AmcrestCamera
from amcrest.exceptions import CommError

from unifi.cams.base import (
    AVClientRequest,
    RetryableError,
    SmartDetectObjectType,
    UnifiCamBase,
)


class DahuaCam(UnifiCamBase):
    def __init__(self, args: argparse.Namespace, logger: logging.Logger) -> None:
        super().__init__(args, logger)
        self.snapshot_dir = tempfile.mkdtemp()
        if self.args.snapshot_channel is None:
            self.args.snapshot_channel = self.args.channel - 1
        if self.args.motion_index is None:
            self.args.motion_index = self.args.snapshot_channel

        self.camera = AmcrestCamera(
            self.args.ip, 80, self.args.username, self.args.password
        ).camera

    @classmethod
    def add_parser(cls, parser: argparse.ArgumentParser) -> None:
        super().add_parser(parser)
        parser.add_argument(
            "--username",
            "-u",
            required=True,
            help="Camera username",
        )
        parser.add_argument(
            "--password",
            "-p",
            required=True,
            help="Camera password",
        )
        parser.add_argument(
            "--channel",
            "-c",
            required=False,
            type=int,
            default=1,
            help="Camera channel",
        )
        parser.add_argument(
            "--snapshot-channel",
            required=False,
            type=int,
            default=None,
            help="Snapshot channel",
        )
        parser.add_argument(
            "--main-stream",
            required=False,
            type=int,
            default=0,
            help="Main Stream subtype index",
        )
        parser.add_argument(
            "--sub-stream",
            required=False,
            type=int,
            default=1,
            help="Sub Stream subtype index",
        )
        parser.add_argument(
            "--motion-index",
            required=False,
            type=int,
            default=None,
            help="VideoMotion event index",
        )
        parser.add_argument(
            "--ptz",
            required=False,
            type=bool,
            default=False,
            help="Camera has ptz support",
        )

    async def get_snapshot(self) -> Path:
        img_file = Path(self.snapshot_dir, "screen.jpg")
        try:
            snapshot = await self.camera.async_snapshot(
                channel=self.args.snapshot_channel
            )
            with img_file.open("wb") as f:
                f.write(snapshot)
        except CommError as e:
            self.logger.warning("Could not fetch snapshot", exc_info=e)
            pass
        return img_file

    async def run(self) -> None:
        if self.args.motion_index == -1:
            return
        while True:
            self.logger.info("Connecting to motion events API")
            try:
                async for event in self.camera.async_event_actions(
                    eventcodes="VideoMotion,SmartMotionHuman,SmartMotionVehicle"
                ):
                    code = event[0]
                    action = event[1].get("action")
                    index = event[1].get("index")

                    if not index or int(index) != self.args.motion_index:
                        self.logger.debug(f"Skipping event {event}")
                        continue

                    object_type = None
                    if code == "SmartMotionHuman":
                        object_type = SmartDetectObjectType.PERSON
                    elif code == "SmartMotionVehicle":
                        object_type = SmartDetectObjectType.VEHICLE

                    if action == "Start":
                        self.logger.info(f"Trigger motion start for index {index}")
                        await self.trigger_motion_start(object_type)
                    elif action == "Stop":
                        self.logger.info(f"Trigger motion end for index {index}")
                        await self.trigger_motion_stop()
            except (CommError, httpx.RequestError):
                self.logger.error("Motion API request failed, retrying")

    async def get_stream_source(self, stream_index: str) -> str:
        if stream_index == "video1":
            subtype = self.args.main_stream
        else:
            subtype = self.args.sub_stream
        try:
            return await self.camera.async_rtsp_url(
                channel=self.args.channel, typeno=subtype
            )
        except (CommError, httpx.RequestError):
            raise RetryableError("Could not generate RTSP URL")

    async def process_continuous_move(self, msg: AVClientRequest) -> None:
        if not self.args.ptz:
            return
        headers = {"Authorization": "Basic "}  # noqa: F841 - reserved for future use
        x = msg["payload"].get("x")
        y = msg["payload"].get("y")
        z = msg["payload"].get("z")

        if x == 0 and y == 0 and z == 0:
            self.camera.ptz_control_command(
                action="stop", code="Left", arg1=0, arg2=1, arg3=0
            )
        elif z > 0:
            self.camera.ptz_control_command(
                action="start", code="ZoomTele", arg1=0, arg2=1, arg3=0
            )
        elif z < 0:
            self.camera.ptz_control_command(
                action="start", code="ZoomWide", arg1=0, arg2=1, arg3=0
            )
        elif y > x and y > 0:
            self.camera.ptz_control_command(
                action="start", code="Up", arg1=0, arg2=1, arg3=0
            )
        elif y < x and y < 0:
            self.camera.ptz_control_command(
                action="start", code="Down", arg1=0, arg2=1, arg3=0
            )
        elif x > y and x > 0:
            self.camera.ptz_control_command(
                action="start", code="Right", arg1=0, arg2=1, arg3=0
            )
        elif x < y and x < 0:
            self.camera.ptz_control_command(
                action="start", code="Left", arg1=0, arg2=1, arg3=0
            )

    async def get_feature_flags(self) -> dict[str, Any]:
        return {
            **await super().get_feature_flags(),
            **{
                "mic": True,
                "ptz": self.args.ptz,
                "smartDetect": [
                    "person",
                    "vehicle",
                ],
            },
        }
