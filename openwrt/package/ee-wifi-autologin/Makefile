include $(TOPDIR)/rules.mk

PKG_NAME:=ee-wifi-autologin
PKG_RELEASE:=1

PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk

define Package/ee-wifi-autologin
  SECTION:=net
  CATEGORY:=Network
  TITLE:=EE WiFi auto-login service
  DEPENDS:=+python3 +python3-requests +python3-certifi +ca-bundle
endef

define Package/ee-wifi-autologin/description
 Lightweight Python daemon that monitors connectivity and triggers EE WiFi captive-portal logins.
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) ./files/* $(PKG_BUILD_DIR)/
endef

define Build/Compile
endef

define Package/ee-wifi-autologin/install
	$(INSTALL_DIR) $(1)/usr/share/ee-wifi-autologin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/usr/share/ee-wifi-autologin/ee_wifi_autologin.py $(1)/usr/share/ee-wifi-autologin/
	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/etc/init.d/ee-wifi-autologin $(1)/etc/init.d/
	$(INSTALL_DIR) $(1)/etc
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/etc/ee-wifi-autologin.json.example $(1)/etc/ee-wifi-autologin.json.example
endef

$(eval $(call BuildPackage,ee-wifi-autologin))
