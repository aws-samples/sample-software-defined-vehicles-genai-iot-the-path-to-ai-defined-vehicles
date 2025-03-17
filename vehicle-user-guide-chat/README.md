# Vehicle User Guide Chat Application
In this example we will go through the steps required to fine-tune a LLM on AWS using SageMaker, optimize it for size targeting edge use case, develop a chat application for a GenAI based vehicle user guide, and deploy to a physical device using AWS IoT Greengrass. Please read the corresponding blog located [here](https://aws.amazon.com/blogs/industries/software-defined-vehicles-genai-iot-the-path-to-ai-defined-vehicles/)
## Running the notebook
You can run the notebook located in the [notebook directory](/vehicle-user-guide-chat/notebook) of this repository using Amazon SageMaker Studio.  
The notebook uses the @remote decorator approach. For additional information on using @remote decorator, take a look at the AWS Blog [Fine-tune Falcon 7B and other LLMs on Amazon SageMaker with @remote decorator](https://aws.amazon.com/blogs/machine-learning/fine-tune-falcon-7b-and-other-llms-on-amazon-sagemaker-with-remote-decorator/).
The notebook included here in this vehicle user guide example is inspired by [amazon-sagemaker-llm-fine-tuning-remote-decorator](https://github.com/aws-samples/amazon-sagemaker-llm-fine-tuning-remote-decorator)
### Prerequisites
The notebook is currently using the latest [HuggingFace](https://github.com/aws/deep-learning-containers/blob/master/available_images.md) Training Container available for the region us-east-1. If you are running the notebook in a different region, make sure to update the ImageUri in the file [config.yaml](/vehicle-user-guide-chat/notebook/config.yaml)
The demo uses huggingface-pytorch-training:2.1.0-transformers4.36.0-gpu-py310-cu121-ubuntu20.04 as the remote trainng container. You can create a custom Docker image for use in the Studio's Jupyterlab spaces, that matches the remote container environment. A [Dockerfile](/vehicle-user-guide-chat/notebook/custom-image) to create a custom image has been provided. You can use this Dockerfile together with these [instructions](https://docs.aws.amazon.com/sagemaker/latest/dg/studio-updated-jl-provide-users-with-images.html) to create and use the custom image. You can use ml.t3.medium instance type in Studio's JupyterLab spaces for this custom image. 
### Dataset
#### [demo-car-data-train_2.csv.gz](/vehicle-user-guide-chat/notebook)
This synthetic dataset has been created using the authors general know-how about cars.
|question|answer|
|--------|------|
|I see a red color horseshoe shape with an exclamation indicator in my car dashboard, what should I do?|It means one or more tires is low on air. Stop the vehicle safely. Find and address the source of air leak.|
|I see a gas tank indicator displayed in my car dashboard, what should I do?|Fuel is low in the vehicle. Refuel at the next opportunity.|
|I see a wrench indicator displayed in my car, what should I do?|It means the vehicle is due for service. Please get the vehicle serviced from an authorized dealer.|
|How do I lower the intensity of the interior lights in this car?|There is a knob to the left of the steering wheel to adjust the intensity of the interior lights.|
## Running the chat application on Amazon EC2 instance
Spin up an EC2 instance on your AWS account, with instance type such as t3.xlarge. You can use eLxr as the operating system for the EC2 instance, using the AMI from AWS Marketplace available [here](https://aws.amazon.com/marketplace/pp/prodview-7z4i6ni24l7bg?applicationId=AWS-Marketplace-Console&ref_=beagle&sr=0-1).
ssh to the EC2 instance. For the eLxr OS, elxr is the login name. Clone this git repository which has the code for the vehicle user guide gen ai application. 
### Quantize the model
On the EC2 instance, [install aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Create a directory called quantize under your home directory or other suitable location. The finetuned model from SageMaker is available at this S3 path (please replace the placeholder values in this url): s3://sagemaker-[AWS Region]-[AWS Account #]/train-TinyLlama-1-1B-Chat-v1-0-[datetime]/train-TinyLlama-1-1B-Chat-v1-0-[datetime]/output/model.tar.gz. Use the aws s3 cp command to copy the model down to the EC2 instance. 
After extracting the contents of the file into the quantize directory, you can use Ollama to quantize the model. We preferred Ollama, as it boosts productivity for completing the task. You will need a standard Docker installation. Run the command from the quantize directory that you created above \
sudo docker run --rm -v .:/model ollama/quantize -q q4_K_M /model \
which will create f16.bin and q4_K_M.bin files. We used the q4_K_M method which provided good size benefits and accuracy. You can experiment other quantization methods available. Copy the q4_K_M.bin to the vehicle-user-guide-chat/chat-application/model directory. 
### Create / run the chat application
The python code for the chat application is in the chat-application directory of this git repository. All necessary pip packages needed are in the requirements.txt file. \
Create a python virtual environment in the vehicle-user-guide-chat/chat-application directory:\
Install python3-venv:\
sudo apt install python3.11-venv

Create the virtual environment:\
python3 -m venv .venv

Activate the virtual environment:\
source .venv/bin/activate

Update pip:\
pip install --upgrade pip

See [Installation requirements for llama-cpp-python](https://github.com/abetlen/llama-cpp-python). Install build-essential to satisfy the llama-cpp-python build requirements:\
sudo apt install build-essential

Install git as this is needed for the llama-cpp-python build:\
sudo apt install git

Install the required python packages:\
pip install -r requirements.txt

Run the server.py Flask application as follows, where the first parameter is the port and the second parameter is the path to the quantized model:\
python3 server.py 8000 ./model/q4_K_M.bin

Launch another ssh session to the EC2 instance - this is to run the client application. Activate the python virtual environment as described above. 
From the vehicle-user-guide-chat/chat-application directory, run the following where the first parameter is the hostname and the second parameter is the port:\
python3 client.py localhost 8000\
You can now try the questions that are in the demo-car-data-train_2.csv, such as What is the height of this car?. You can exit the application by typing exit
## Running the chat application on ARM Virtual Hardware (AVH)
Please refer to [AVH documentation](https://support.avh.corellium.com/getting-started/) on how to spin up a virtual device instance. You will need a compatible eLxr OS image to boot into the virtual NXP i.MX 8M Plus device. Please contact Wind River, who contributed the initial eLxr release, to obtain the eLxr OS image for AVH.
Once the device is booted, the instructions to run the application are the same as running the chat application on the Amazon EC2 instance described above.
## Deploying the application to the physical device using AWS IoT Greengrass
You can use the standard Greengrass device setup and deployment process to deploy the application on to the physical device. 
For setting up the device, please refer to the documentation [here](https://docs.aws.amazon.com/greengrass/v2/developerguide/setting-up.html). 
For creating and deploying the component, please refer to the documentation [here](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-components.html).
The greengrass folder in the repository has the complete list of supporting files that you can use to create the deployment. You can initiatilze a python based component using gdk cli as shown [here](https://docs.aws.amazon.com/greengrass/v2/developerguide/create-components.html). You can then copy the files provided in the greengrass directory of this repository to create the component. The files refer to the component as slm-ug which is short for Small Language Model based User Guide. You can change it to any name of your choice. Make the following adjustments to few of the files as follows:
* In the gdk-config.json file, update the author, bucket, region and zip_name to your preferred values, and set the componentVersion to a value of your choice.
* In the deployment.json file, specify your device arn, update the component name to match what you have specified in the gdk-config.json, and set the componentVersion to a value of your choice.
* In the recipe.yaml file, update the componentname and componentversion to match what you have specified in the gdk-config.json, update componentpublisher, and fix the URI to match your s3 bucket name, componentname and component version. Fix the component path in the Lifecycle section to match your updates from the above areas. Please note that install.sh that is referenced in this recipe file is already created for you and available in the same greengrass directory.

You will need a compatible eLxr OS image to boot into the physical NXP i.MX 8M Plus device. Please contact Wind River, who contributed the initial eLxr release, to obtain the special eLxr OS image. You may need to install build-essential and git using apt, as the greengrass deployment expects these tools to be present for a successful compilation of llama-cpp-python. The author did obtain the eLxr OS from Wind River and tested the Greengrass deployment and the functioning of the application successfully, on a physical NXP i.MX 8M device. \
\
The greengrass deployment runs server.py as a service. Assuming greengrass has been setup in a /mnt/emmc-drive/greengrass/ directory, the client can be run as follows:
* source /mnt/emmc-drive/greengrass/v2/work/com.amazon.SlmUserGuide/venv/bin/activate
* cd /mnt/emmc-drive/greengrass/v2/packages/artifacts-unarchived/com.amazon.SlmUserGuide/1.0.2/com.amazon.SlmUserGuide
* python3 client.py
