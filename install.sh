mkdir temp
cd temp

# Install required libs
sudo apt install -y libopenjp2-7 libtiff5

# Install wiringpi
sudo apt-get install wiringpi
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v

# Install bcm2835-1.60
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz 
cd bcm2835-1.60/
sudo ./configure
sudo make && sudo make check && sudo make install
cd ..

# Install waveshare lib
sudo git clone https://github.com/waveshare/e-Paper.git
sudo mv 'e-Paper/RaspberryPi_JetsonNano/python/lib' ../lib

# Install pip and requirements
sudo apt-get update
sudo apt-get install -y python3-pip
sudo pip3 install -r ../requirements.txt

# remove temp folder
cd ..
sudo rm -rf temp
