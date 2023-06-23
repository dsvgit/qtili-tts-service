# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "kazakh-tts"
  config.vm.provider "virtualbox" do |vb|
    vb.name = "kazakh-tts"
    vb.memory = "4096"
  end

  config.vm.synced_folder ".", "/vagrant_data"
  config.vm.network "forwarded_port", guest: 3000, host: 3000

  config.vm.provision "shell", :path => "bootstrap.sh"
end
