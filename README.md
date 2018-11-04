# pouch-rpm
rpm package for pouch container

test under centos 7 x64 only, at your own risk.

## quickstart
```
#download RPMS directly  
yum localinstall lxcfs-2.0.8-1.el7.x86_64.rpm pouch-1.0.0-3.el7.x86_64.rpm -y  
systemctl enable lxcfs pouch  
systemctl start lxcfs pouch  
```
## howtobuild
#### prepare
```
yum-config-manager --add-repo https://mirror.go-repo.io/centos/go-repo.repo  
yum install golang -y  
yum install rpm-build wget git -y  
```
#### build pouch
```
cd ~  
git clone https://github.com/purplegrape/pouch-rpm rpmbuild  
cd rpmbuild/SPEC  
rpmbuild -ba lxcfs  
rpmbuild -ba pouch  
```
