# Copyright 2023 Marcel Bollmann <marcel@bollmann.me>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Global configuration settings."""

from attrs import define
from omegaconf import OmegaConf


@define
class DefaultConfig:
    url_prefix: str = "${oc.env:ANTHOLOGY_PREFIX,https://aclanthology.org}"
    """Prefix for all remote URLs. Can also be overridden with the environment variable `ANTHOLOGY_PREFIX`."""

    pdf_location_template: str = "${url_prefix}/{}.pdf"
    """URL formatting template for paper PDFs."""

    pdf_thumbnail_location_template: str = "${url_prefix}/thumb/{}.jpg"
    """URL formatting template for paper thumbnail images."""

    attachment_location_template: str = "${url_prefix}/attachments/{}"
    """URL formatting template for paper attachments."""

    event_location_template: str = "${url_prefix}/{}"
    """URL formatting template for event-related files."""

    video_location_template: str = "${url_prefix}/{}"
    """URL formatting template for videos."""


config = OmegaConf.structured(DefaultConfig)
"""Configuration instance that is used by all `acl_anthology` classes."""