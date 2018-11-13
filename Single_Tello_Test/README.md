# Single_Tello_Test
## Step1
Write the command set to be run in command.txt, for example:：
```
command
takeoff
land
```
## Step2
The script will automatically send a command to Tello. After receiving the reply from the previous command, the next command will be sent immediately.
To add a delay, you can use the Delay command and the script will automatically delay. The unit of delay is seconds, which can be given to decimals.
```
delay 5
```
## Step3
Run the script
```
python tello_test.py command.txt
```
The command window will type each instruction and its reply. After the execution is finished, the commands will be stored in the log folder to name the test end time.
