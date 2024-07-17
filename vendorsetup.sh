color="\033[1;36m"
end="\033[0m"

# Vendor & Kernel Sources
echo -e "${color}Cloning vendor${end}"
git clone --depth=1 -b udc https://github.com/ihsanulrahman/vendor_xiaomi_miatoll vendor/xiaomi/miatoll

echo -e "${color}Cloning kernel${end}"
git clone --depth=1 -b universe https://github.com/BlissRoms-Devices/android_kernel_xiaomi_sm6250 kernel/xiaomi/sm6250

sleep 1

# Lineage-21 Hardware Source
echo -e "${color}Cloning Hardware & Timekeep from Lineage-21${end}"
rm -rf hardware/xiaomi
git clone https://github.com/LineageOS/android_hardware_xiaomi -b lineage-21 hardware/xiaomi 
git clone https://github.com/LineageOS/android_hardware_sony_timekeep -b lineage-21 hardware/sony/timekeep

sleep 1