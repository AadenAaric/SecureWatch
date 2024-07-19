# **AI-Powered Residential Surveillance System**
Our AI-Powered Residential Surveillance System is designed to enhance security and peace of mind for homeowners and property managers. Utilizing advanced artificial intelligence and machine learning technologies, this system offers real-time monitoring of people entering and leaving a residential area.

# **Project Structure**
The project is organized into several Django apps, each responsible for different aspects of the system's functionality. Here is a brief overview of the primary apps in the project:

# **General**
The General app contains the general REST APIs required for the overall functioning of the surveillance system. This includes APIs for user authentication, user management, and other common functionalities that are shared across the system.

# **video_streamer**
The video_streamer app handles video streaming. This app is responsible for managing multiple camera resources, capturing and processing video frames, and providing live streaming capabilities. It also includes functionalities for face detection, recognition, and tracking.

# **notification**
The notification app manages notifications over WebSockets. This app is responsible for real-time communication between the server and clients, ensuring timely delivery of alerts and updates. It integrates with the system to notify users about important events, such as the detection of unrecognized individuals or other security alerts.

By structuring the project into these apps, we ensure a modular and organized approach, making the system easier to manage, maintain, and extend.

# **Getting Started**
To get the AI-Powered Residential Surveillance System up and running, follow these steps:

# **Prerequisites**
Make sure you have the following installed on your system:

Python 3.10+
Django
Django Channels (for WebSockets)
OpenCV
Other dependencies as specified in the requirements.txt file
Installation
Clone the repository:

**bash**
`Copy code
git clone <repository-url>
cd <repository-directory>`
Install dependencies:

**bash**
`Copy code
pip install -r requirements.txt`
Setup the database:

**bash**
`Copy code
python manage.py makemigrations
python manage.py migrate
`


Run the development server:

**bash**
`Copy code
python manage.py runserver`

Running the Server
Once you have completed the installation steps, you can start the server using the following command:

**bash**
`Copy code
python manage.py runserver`
The development server will start, and you can access the application in your web browser at http://127.0.0.1:8000/.

**WebSocket Server**
For the notification app to handle real-time notifications, you need to run the Django Channels server. Make sure daphne is installed and use the following command:


**Accessing the Admin Interface**
To manage users, cameras, and other settings, access the Django admin interface at http://127.0.0.1:8000/ and log in with the superuser credentials you created earlier.
**
Additional Configuration**
Camera Setup: Configure your cameras in the video_streamer app to start streaming and processing video.
Notification Setup: Ensure the WebSocket server is running to handle real-time notifications in the notification app.
By following these steps, you will have a functional AI-Powered Residential Surveillance System ready for real-time monitoring and notifications.
