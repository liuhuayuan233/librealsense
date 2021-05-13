# License: Apache 2.0. See LICENSE file in root directory.
# Copyright(c) 2021 Intel Corporation. All Rights Reserved.

# test:device L500*
# test:device D400*

import pyrealsense2 as rs
from rspy import test

d400_fw_min_version_1 = 'Signed_Image_UVC_5_8_15_0.bin'
d400_fw_min_version_2 = 'Signed_Image_UVC_5_12_7_100.bin'
d400_fw_min_version_3 = 'Signed_Image_UVC_5_12_12_100.bin'
d400_fw_min_version_1_prev = 'Signed_Image_UVC_5_8_14_0.bin'
d400_fw_min_version_2_prev = 'Signed_Image_UVC_5_12_6_0.bin'
d400_fw_min_version_3_prev = 'Signed_Image_UVC_5_12_11_0.bin'

l500_fw_min_version = 'Signed_Image_UVC_1_4_1_0.bin'
l500_fw_min_version_prev = 'Signed_Image_UVC_1_4_0_10.bin'

sr300_fw_min_version_1 = 'Signed_Image_UVC_3_26_1_0.bin'
sr300_fw_min_version_2 = 'Signed_Image_UVC_3_27_1_0.bin'
sr300_fw_min_version_1_prev = 'Signed_Image_UVC_3_21_0_0.bin'
sr300_fw_min_version_2_prev = 'Signed_Image_UVC_3_26_3_0.bin'
pid_to_min_fw_version = {#D400 product line:
                         '0AD1': d400_fw_min_version_1,  # D400
                         '0AD2': d400_fw_min_version_1,  # D410
                         '0AD3': d400_fw_min_version_1,  # D415
                         '0AD4': d400_fw_min_version_1,  # D430
                         '0AD5': d400_fw_min_version_1,  # D430_MM
                         '0AD6': d400_fw_min_version_1,  # USB2
                         '0ADB': d400_fw_min_version_1,  # RECOVERY
                         '0ADC': d400_fw_min_version_1,  # USB2_RECOVERY
                         '0AF2': d400_fw_min_version_1,  # D400_IMU
                         '0AF6': d400_fw_min_version_1,  # D420
                         '0AFE': d400_fw_min_version_1,  # D420_MM
                         '0AFF': d400_fw_min_version_1,  # D410_MM
                         '0B00': d400_fw_min_version_1,  # D400_MM
                         '0B01': d400_fw_min_version_1,  # D430_MM_RGB
                         '0B03': d400_fw_min_version_1,  # D460
                         '0B07': d400_fw_min_version_1,  # D435
                         '0B0C': d400_fw_min_version_1,  # D405U
                         '0B3A': d400_fw_min_version_2,  # D435I
                         '0B49': d400_fw_min_version_1,  # D416
                         '0B4B': d400_fw_min_version_1,  # D430I
                         '0B4D': d400_fw_min_version_1,  # D465
                         '0B52': d400_fw_min_version_1,  # D416_RGB
                         '0B5B': d400_fw_min_version_3,  # D405
                         '0B5C': d400_fw_min_version_2,   # D455
                        #L500 product line:
                         '0B55': l500_fw_min_version,  # L500_RECOVERY
                         '0B72': l500_fw_min_version,  # L535_RECOVERY
                         '0ADC': l500_fw_min_version,  # L500_USB2_RECOVERY_OLD
                         '0B0D': l500_fw_min_version,  # L500
                         '0B3D': l500_fw_min_version,  # L515_PRE_PRQ
                         '0B64': l500_fw_min_version,  # L515
                         '0B68': l500_fw_min_version,  # L535
                        #SR300 product line:
                         '0AA3': sr300_fw_min_version_2,  # SR306
                         '0AA5': sr300_fw_min_version_1,  # SR300
                         '0B48': sr300_fw_min_version_1,  # SR300v2
                         '0AB3': sr300_fw_min_version_1   # SR300_RECOVERY
                         }


sr300_fw_max_version_1 = 'Signed_Image_UVC_3_26_1_0.bin'
sr300_fw_max_version_2 = 'Signed_Image_UVC_3_27_0_0.bin'

pid_to_max_fw_version = {#SR300 product line:
                         #'0AA3': dummy_fw_max_version,   SR306
                         '0AA5': sr300_fw_max_version_2,  # SR300
                         '0B48': sr300_fw_max_version_1,  # SR300v2
                         '0AB3': sr300_fw_max_version_1   # SR300_RECOVERY
                         }

fw_previous_version = {d400_fw_min_version_1: d400_fw_min_version_1_prev,
                       d400_fw_min_version_2: d400_fw_min_version_2_prev,
                       d400_fw_min_version_3: d400_fw_min_version_3_prev,
                       l500_fw_min_version:l500_fw_min_version_prev,
                       sr300_fw_min_version_1:sr300_fw_min_version_1_prev,
                       sr300_fw_min_version_2:sr300_fw_min_version_2_prev
}


def check_firmware_not_compatible(updatable_device, fw_image):
    test.check(not updatable_device.check_firmware_compatibility(fw_image))


def check_firmware_compatible(updatable_device, fw_image):
    test.check(updatable_device.check_firmware_compatibility(fw_image))


ctx = rs.context()
dev = ctx.query_devices()[0]
updatable_device = dev.as_updatable()

#############################################################################################
test.start("checking firmware compatibility with device")
pid = dev.get_info(rs.camera_info.product_id)
print(dev.get_info(rs.camera_info.name) + " found")
min_fw_version = pid_to_min_fw_version[pid]
one_before_min_fw_version = fw_previous_version[min_fw_version]
print("fw min version: " + min_fw_version + ", one before: " + one_before_min_fw_version)
with open(one_before_min_fw_version, 'rb') as binary_file:
    fw_image = bytearray(binary_file.read())
    check_firmware_not_compatible(updatable_device, fw_image)

with open(min_fw_version, 'rb') as binary_file:
    fw_image = bytearray(binary_file.read())
    check_firmware_compatible(updatable_device, fw_image)

test.finish()
test.print_results_and_exit()
