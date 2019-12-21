echo "DEPLOY START!!"

# Input your function name
funcname="alexaFunctionForTello"

docker run --rm -v "$PWD":/var/task shoda888/local2pylambda:latest
aws lambda update-function-code --function-name ${funcname} --zip-file fileb://deploy_package.zip --profile syspro