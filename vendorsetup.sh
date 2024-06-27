git clone --depth=1 -b main https://github.com/c0smic-Lab/kernel_xiaomi_sm6250 kernel/xiaomi/sm6250
git clone --depth=1 -b udc https://github.com/ihsanulrahman/vendor_xiaomi_miatoll vendor/xiaomi/miatoll
rm -rf hardware/xiaomi
git clone https://github.com/LineageOS/android_hardware_xiaomi -b lineage-21 hardware/xiaomi 
git clone https://github.com/LineageOS/android_hardware_sony_timekeep -b lineage-21 hardware/sony/timekeep