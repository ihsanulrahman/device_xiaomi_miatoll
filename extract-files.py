#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024-2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/miatoll',
    'hardware/qcom-caf/sm8150',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    if partition.startswith('_'):
        partition = partition[1:]  # Remove leading underscore

    if partition not in ('vendor', 'system'):
        return None

    return f'{lib}_{partition}'

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'libmmosal',
        'vendor.qti.hardware.fm@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.imsrtpservice@3.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/etc/camera/camxoverridesettings.txt': blob_fixup()
        .regex_replace('0x10082', '0')
        .regex_replace('0x1F', '0x0'),
    'vendor/etc/init/android.hardware.keymaster@4.0-service-qti.rc': blob_fixup()
        .regex_replace('@4.0', '@4.1'),
    ('vendor/lib64/camera/components/com.qti.node.dewarp.so', 'vendor/lib64/camera/components/com.vidhance.node.eis.so'): blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so'),
    'vendor/lib64/camera/components/com.qti.node.watermark.so': blob_fixup()
        .add_needed('libpiex_shim.so'),
    'vendor/lib64/hw/fingerprint.fpc.default.so': blob_fixup()
        .sig_replace('30 00 00 90 11 3A 42 F9', '30 00 00 90 1F 20 03 D5'),
    ('vendor/lib64/libalAILDC.so', 'vendor/lib64/libalLDC.so', 'vendor/lib64/libalhLDC.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    ('vendor/lib64/libhvx_interface.so', 'vendor/lib64/libmialgo_rfs.so', 'vendor/lib64/libVDSuperPhotoAPI.so', 'vendor/lib64/libsnpe_dsp_domains_v2.so'): blob_fixup()
        .clear_symbol_version('remote_handle_close')
        .clear_symbol_version('remote_handle_invoke')
        .clear_symbol_version('remote_handle_open')
        .clear_symbol_version('remote_handle64_close')
        .clear_symbol_version('remote_handle64_invoke')
        .clear_symbol_version('remote_handle64_open')
        .clear_symbol_version('remote_register_dma_handle')
        .clear_symbol_version('remote_register_buf_attr')
        .clear_symbol_version('remote_register_buf'),
    'vendor/lib64/libgoodixhwfingerprint.so': blob_fixup()
        .replace_needed('libvendor.goodix.hardware.biometrics.fingerprint@2.1.so', 'vendor.goodix.hardware.biometrics.fingerprint@2.1.so'),
    'vendor/lib64/libwvhidl.so': blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'system_ext/etc/init/wfdservice.rc': blob_fixup()
        .regex_replace(r'(start|stop) wfdservice\b', r'\1 wfdservice64'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .remove_needed('android.hidl.base@1.0.so'),
    ### Dolby Codec2 (cancunf) Start ###
    ('vendor/lib64/libcodec2_soft_ac4dec.so', 'vendor/lib64/libcodec2_soft_ddpdec.so', 'vendor/lib64/libdeccfg.so'): blob_fixup()
        .replace_needed('vendor.dolby.hardware.dms@2.0.so', 'vendor.dolby.hardware.dms@2.0-v34_cancunf.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v34_cancunf.so')
        .replace_needed('libdapparamstorage.so', 'libdapparamstorage-v34_cancunf.so'),
    ### Dolby Codec2 (cancunf) End ###
    ### Dolby Equalizer (rhode) Start ###
    ('vendor/lib64/libdlbdsservice.so'): blob_fixup()
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v32_rhode.so'),
    ### Dolby Equalizer (rhode) End ###
}  # fmt: skip

module = ExtractUtilsModule(
    'miatoll',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

# --- Cleanup Unlisted Blobs ---
ANDROID_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
PROP_DIR = os.path.join(ANDROID_ROOT, "vendor/xiaomi/miatoll/proprietary")
PROP_FILES_TXT = os.path.join(os.path.dirname(__file__), "proprietary-files.txt")

def get_expected_files():
    """Read proprietary-files.txt and return a set of expected file paths, ignoring SHA1SUM values and metadata."""
    expected_files = set()
    
    if not os.path.exists(PROP_FILES_TXT):
        print(f"Warning: {PROP_FILES_TXT} not found.")
        return expected_files

    with open(PROP_FILES_TXT, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Ignore empty lines and comments
            
            # Extract part before | (to remove SHA1SUM) and before ; (to remove metadata)
            file_paths = line.split("|")[0].split(";")[0]

            # Split multiple paths by ':'
            for path in file_paths.split(":"):
                expected_files.add(path.lstrip("-"))  # Remove leading '-' if present

    return expected_files

def cleanup_unlisted_blobs():
    """Remove unlisted blobs from the proprietary folder."""
    if not os.path.exists(PROP_DIR):
        return

    expected_files = get_expected_files()

    for root, _, files in os.walk(PROP_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, PROP_DIR)

            # Ignore .part files silently
            if ".part" in file:
                continue

            if rel_path not in expected_files:
                print(f"Removing unlisted blob: {file_path}")
                os.remove(file_path)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
    cleanup_unlisted_blobs()  # Run cleanup after extraction
