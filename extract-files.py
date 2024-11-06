#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024-2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/camera/camxoverridesettings.txt': blob_fixup()
        .regex_replace('0x10082', '0')
        .regex_replace('0x1F', '0x0'),
    'vendor/etc/init/android.hardware.keymaster@4.0-service-qti.rc': blob_fixup()
        .regex_replace('@4.0', '@4.1'),
    'vendor/lib64/camera/components/com.qti.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    'vendor/lib64/hw/fingerprint.fpc.default.so': blob_fixup()
        .sig_replace('30 00 00 90 11 3A 42 F9', '30 00 00 90 1F 20 03 D5'),
    'vendor/lib64/android.hardware.camera.provider@2.4-legacy.so': blob_fixup()
        .add_needed('libcamera_provider_shim.so'),
    'system_ext/etc/init/wfdservice.rc': blob_fixup()
        .regex_replace(r'(start|stop) wfdservice\b', r'\1 wfdservice64'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .remove_needed('android.hidl.base@1.0.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm6250-common',
    'xiaomi',
    blob_fixups=blob_fixups,
    check_elf=False,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
