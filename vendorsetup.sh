color="\033[1;36m"
end="\033[0m"

# Common DT
echo -e "${color}Cloning Common DT${end}"
git clone -b 13 https://github.com/ihsanulrahman/device_xiaomi_sm6250-common device/xiaomi/sm6250-common

# Vendor & Kernel Sources
echo -e "${color}Cloning vendor${end}"
git clone --depth=1 -b 13 https://github.com/ihsanulrahman/vendor_xiaomi_miatoll vendor/xiaomi/miatoll
git clone --depth=1 -b 13 https://github.com/ihsanulrahman/vendor_xiaomi_sm6250-common vendor/xiaomi/sm6250-common

echo -e "${color}Cloning kernel${end}"
git clone --depth=1 -b old-nonksu https://github.com/ihsanulrahman/android_kernel_xiaomi_sm6250 kernel/xiaomi/sm6250

sleep 1

# Hardware Sources
echo -e "${color}Cloning Hardware & Timekeep ${end}"
rm -rf hardware/xiaomi
git clone https://github.com/LineageOS/android_hardware_xiaomi -b lineage-20 hardware/xiaomi 
git clone https://github.com/LineageOS/android_hardware_sony_timekeep -b lineage-20 hardware/sony/timekeep

# Miui Camera
echo -e "${color}Cloning Miui Camera${end}"
git clone https://gitlab.com/userariii/vendor-xiaomi-miuicamera.git -b Tiramisu vendor/xiaomi/miuicamera

sleep 1