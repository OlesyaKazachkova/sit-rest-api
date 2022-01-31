cd ..
source devenv/bin/activate
sh build.sh
git add .
git commit -m "script deploy_dev"
git push origin master

