sudo apt update
sudo apt upgrade -y
sudo apt install -y git git-lfs python3-pip python3-tk vlc
pip3 install --upgrade pip
sudo -H pip3 install --upgrade ipython Pillow pygame screeninfo python-vlc

DESKTOP_PATH=/home/mada/Desktop # $HOME/Desktop
cat > $DESKTOP_PATH/Neuron.desktop <<EOF
[Desktop Entry]
Name=Neuron
Comment=Neuron
Exec=$DESKTOP_PATH/hbp_neuron/run.sh
Version=1.0
Terminal=false
Type=Application
GenericName[en_IL]=Neuron
EOF

# sudo apt install -y python3-pil python3-pil.imagetk
# cd Desktop
# git clone https://github.com/jerusalem-science-museum/hbp_neuron.git
# cd hbp_neuron
# git lfs install
# git lfs pull
