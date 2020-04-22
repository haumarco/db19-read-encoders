# Info:
This repo is based on mech-4640/db-read-encoders. I changed a lot in the encoder_ticks_node.py file since there occured some bugs. I also changed the installation of the pigpio. The rest is more or less the same.
To read the code you need to have the EncoderTicksStamped.msg file in dt-ros-commons. Since it's not in the master branch yet, you can download it from haumarco/dt-ros-commons.

    build it:
    $ dts devel build -f --arch arm32v7
    run it:
    $ docker -H ueli.local run --name read_encoders -it --rm --privileged --net=host duckietown/db19-read-encoders:v1-arm32v7

# Template: template-ros

This template provides a boilerplate repository
for developing ROS-based software in Duckietown.

**NOTE:** If you want to develop software that does not use
ROS, check out [this template](https://github.com/duckietown/template-basic).


## How to use it

### 1. Fork this repository

Use the fork button in the top-right corner of the github page to fork this template repository.


### 2. Create a new repository

Create a new repository on github.com while
specifying the newly forked template repository as
a template for your new repository.


### 3. Define dependencies

List the dependencies in the files `dependencies-apt.txt` and
`dependencies-py.txt` (apt packages and pip packages respectively).


### 4. Place your code

Place your ROS packages in the directory `/packages` of
your new repository.

**NOTE:** Do not use absolute paths in your code,
the code you place under `/packages` will be copied to
a different location later.


### 5. Setup the launchfile

Change the file `launch.sh` in your repository to
launch your code.
