# Cisco SD-WAN vExplore

vExplore is a python script to explore Cisco SD-WAN templates showing a graphical representation of the hierarchical relationship between device templates and feature templates.

# Requirements

To use this code you will need:

- Python 3.7+
- vManage user login details.

# Install and Setup

- Clone the code to local machine.

```
git clone https://github.com/HusseinOmar/vExplore.git
cd vExplore
```

- Setup Python Virtual Environment (requires Python 3.7+)

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

- Run application file

```
python3 vExplore.py
```

![image](https://github.com/HusseinOmar/vExplore/blob/main/newplot.png)

# Demo Video

Click Image below

[![Demo Video](https://img.youtube.com/vi/_H3xIVxV-rQ/0.jpg)](https://www.youtube.com/watch?v=_H3xIVxV-rQ)

# License

[CISCO SAMPLE CODE LICENSE - Link](https://developer.cisco.com/docs/licenses)

[Cisco Sample Code License - Local File](LICENSE)

# Caveats

This script use multithreading, this can overwhelm your vManage, the default wait time between API calls is 1 sec by default. If the code fails in certain steps you will need to increase the timer accordingly.

# Questions and Contact Info

If you have any issues or a pull request, you can submit a Issue or contact me directly。

My Cisco CEC ID is: husseino
My email address husseino@cisco.com
