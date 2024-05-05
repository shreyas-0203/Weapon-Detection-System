The Weapon Detection System is a project aimed at enhancing security measures by utilizing state-of-the-art deep learning techniques for real-time weapon detection. The system employs the YOLO (You Only Look Once) algorithm, a powerful object detection model, to identify weapons within images or video streams. Leveraging a pre-trained YOLO model enables accurate and efficient detection of weapons in various environments.

In addition to weapon detection, the system incorporates advanced features for enhanced functionality and situational awareness. A JSON API integration facilitates the retrieval of real-time location details, including latitude, longitude, IP address, and timestamp, when a weapon is detected or triggered. This information can be invaluable for security personnel or law enforcement agencies to respond promptly to potential threats.

To provide a user-friendly interface, the system utilizes Flask, a web framework for Python, to seamlessly integrate the detection capabilities into a frontend application. This integration simplifies the deployment and usage of the weapon detection system, making it accessible to a broader audience.

Readme Details:

Installation:

Clone the repository to your local machine using git clone https://github.com/shreyas-0203/Weapon-Detection-System.git.
Navigate to the project directory.

Usage:

Run the Flask application by executing python main.py.
Access the application through your web browser by visiting http://localhost:5000.
Upload an image or video containing potential weapon objects.
Monitor the output for detected weapons, along with real-time location details retrieved via the JSON API.

Dependencies:

YOLOv3: The project utilizes a pre-trained YOLOv3 model for weapon detection.
Flask: A Python web framework used for building the frontend interface.
JSON API: Integration with a JSON API to retrieve real-time location details.
