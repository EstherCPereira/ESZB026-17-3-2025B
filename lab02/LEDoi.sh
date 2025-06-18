#!/bin/bash


echo 20 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio20/direction

echo 1 > /sys/class/gpio/gpio20/value
sleep 2
echo 0 > /sys/class/gpio/gpio20/value

echo 20 > /sys/class/gpio/unexport

echo 21 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio21/direction

echo 1 > /sys/class/gpio/gpio21/value
sleep 1
echo 0 > /sys/class/gpio/gpio21/value

echo 21 :> /sys/class/gpio/gpio21/
echo out > /sys/class/gpio/unexport




