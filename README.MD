
# CONTINUOUS SPEED TEST

## GOAL:
This is a program that performs a speed test of the internet connection using the speedtest-cli library every x (the time can be adjusted in the settings) minutes. The data is saved and then at a time specified a daoly email is sent containing a graph of the data, a csv file and avarages, min and max values.

The test tracks ping, download and upload speeds.


## use
In the [password file](password.txt) write the email password of the account from which the daily email log will be sent. The username should be set directly in the [plotting.py](plotting.py) file.  

In the [settings.json](settings.json)  file set the parameters for the frequency of the test and of the email time. 

This program can be loaded onto a rasperry py and used with systemd service
In that case "make r" git pulls and restarts it.
"make log" opens journalctl logs.
"make logd" opens journalctl logs for the last day

MADE in Friuli, Italy  by Alberto Girardi
11/06/2024

[![wakatime](https://wakatime.com/badge/user/018b48bf-8d51-471d-b870-e93a045be5f7/project/8239b444-2fd4-4ef4-8166-6acee16ccbff.svg)](https://wakatime.com/badge/user/018b48bf-8d51-471d-b870-e93a045be5f7/project/8239b444-2fd4-4ef4-8166-6acee16ccbff)


updated from the pi too!
