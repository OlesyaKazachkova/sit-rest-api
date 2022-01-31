cd ..
source prodenv/bin/activate
sh build.sh
git add .
git commit -m "script deploy_prod"
git push origin master

