docker run --rm -v "$PWD":/var/task aws-lambda-python3.7-test:latest
aws lambda update-function-code --function-name alexa-to-tellopython --zip-file fileb://deploy_package.zip