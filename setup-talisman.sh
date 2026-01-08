#!/bin/bash
echo "Setting up Talisman pre-commit hook..."

# Download and install Talisman
curl --silent https://raw.githubusercontent.com/thoughtworks/talisman/master/global_install_scripts/install.bash > /tmp/install_talisman.bash
chmod +x /tmp/install_talisman.bash
/tmp/install_talisman.bash pre-commit

echo "Talisman installed successfully!"
echo "Configuration is in .talismanrc"
