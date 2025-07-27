ifneq (,$(filter user, $(TARGET_BUILD_VARIANT)))
BOARD_VENDOR_SEPOLICY_DIRS += $(COMMON_PATH)/sepolicy/diag
endif
