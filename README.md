# pouch-rpm
rpm package for pouch container

test under centos 7 x64 only,at your own risk.

## howto

#### prepare
yum-config-manager --add-repo https://mirror.go-repo.io/centos/go-repo.repo  
yum install golang -y  
yum install rpm-build wget git -y  

#### build pouch
cd ~  
git clone https://github.com/purplegrape/pouch-rpm rpmbuild  
cd rpmbuild/SPEC  
rpmbuild -ba pouch  

