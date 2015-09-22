# TARS
TARS is a mini-robot that navigates using either manual control or artificial intelligence.

# Capabilities
TARS can search for destination using various search algorithms like DFS, BFS, A Star et cetera. The software also consists of a simple visual UI that allows user to configure, deploy and track the movement on a simulated radar.

# Architecture
The application is based purely in python. It is divided in two sections, Client and the Server. The Raspberry Pi on TARS acts as the server while a client can be any device on the network capable of running it. Both communicate via socket programming. <br />
Client has a simple <i>easygui</i> based menu driven interface that allows run-time configuration of variables. It also has a radar that is created using <i>pygame</i> which tracks the bot movement and renders it on client display.

# Software Specs
Language : Python <br />
Server OS : Raspbian / Linux <br />
Client OS : Linux / Windows <br />
Third-party : pygame, easygui RPi.GPIO 

# Hardware 
Raspberry Pi Model B 512 MB  <br />
HC-SR04 Obstacle detector  <br />
RTK Motor Controller Board  <br />
5MP camera  <br />
Raspbian OS  <br />
2 DC Motors  <br />
2 Side wheels  <br />
1 Castor wheel  <br />
Power Source = DNY Power bank

# About us
We are two computer science graduates with interest in Artificial Intelligence, Machine learning and Deep learning. This is a side project driven by curiosity.
For any query, feel free to contact us at :- dograabhimanyu@gmail.com <br />
- Abhimanyu Dogra and Niharika Dutta

# How to run
Download the <i>server</i> folder to Raspberry Pi and run <i>server_main.py</i> to initiate the server.
Download the <i>client</i> folder to the client device and run <i>main.py</i> to run UI application.