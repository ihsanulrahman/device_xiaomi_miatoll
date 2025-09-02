color="\033[1;36m"
end="\033[0m"

# Vendor & Kernel Sources
echo -e "${color}Cloning vendor${end}"
git clone --depth=1 -b 166 https://github.com/ihsanulrahman/vendor_xiaomi_miatoll vendor/xiaomi/miatoll

echo -e "${color}Cloning kernel${end}"
git clone --depth=1 -b 16 https://github.com/ihsanulrahman/android_kernel_xiaomi_sm6250 kernel/xiaomi/sm6250

sleep 1

# Hardware Sources
echo -e "${color}Cloning Hardware & Timekeep ${end}"
rm -rf hardware/xiaomi
git clone https://github.com/ihsanulrahman/hardware_xiaomi -b 16-dolby hardware/xiaomi 
git clone https://github.com/LineageOS/android_hardware_sony_timekeep -b lineage-22.2 hardware/sony/timekeep

# Miui Camera
echo -e "${color}Cloning Miui Camera${end}"
git clone -b 15 https://github.com/ihsanulrahman/vendor_xiaomi_miuicamera vendor/xiaomi/miuicamera

sleep 1
