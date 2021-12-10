

## GUI Functionality
- Allows user to "train on data" by creating .csv files containing data mimicking mouse cursor movement 
- Use mouse data text file to have robot mimick movements from user mouse data and run applications to execute the data
- Allow for configurable state declarations (radians or degree, bounded or unbounded (more than 365)), and what gets saved to .json to have easy IRL algo (behavorial cloning) implemented

## Running the GUI
To use the designed GUI naviagate to the branch_updated_gui folder and download the signature_graphing.py and GUI_Update.py files. 
On line 158 where it has variable "file_to_draw" replace this line with the desired path where you will save your policy when it gets generated, and where the "import policy" button will look when clicked. (a sample character a policy csv is in the folder to test)
 
 ## Start training
- first click the "train" button, name your directory as asked in the terminal, then navigate to the pi game app an start drawing your charecter (left click to start drawing recording, left click let up to stop and refresh drawing page). Draw as many trajectories as desired.
- when done exit out of the application, then navigate back to the pygame gui and 
- make sure you move the policy that was generated from training (in same folder you create) to the file path you specified earlier where the gui will look for the policy 
- click on "import policy" button to get the policy uploaded
- left click in gui to start surgery, lift up left click to have robot mimick based on policy defined from training (can add policy by changing policy in folder and clicking import policy, restart by pressing r, and train again by pressing train )
- at any point right click to have the doctor stop drawing/doing surgery
- pink indicates where cutout time occured and emphasizes the differncces between what the robot and user did

## In order to run scripts
You will need to install python packages. 
In terminal, donwload packages with command
- pip install pyautogui
- pip install tk



# IRLSurgery
Inverse Reinforcement Learning Surgery software simulation.
