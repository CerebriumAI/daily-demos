# Pet detection Demo

## Description

This repository contains code for the Pet detection demo project using Daily and Cerebrium. In this example, we have a bot that monitors each participants screen
for a cat or dog using a YOLOv8 model. If a pet is detected in any participants frame, the bot posts a frame of it to the call with bounding boxes around the pet.

The model trained for this example is extremely basic (trained on 250 examples) and is for demo purposes. We recommend you fine-tune your own model to get more performant results.

## Deployment Instructions
You can deploy the example below in just a few easy steps.
1. Git Clone the repository and make sure you are in the pet-object-detection folder
2. Sign up at https://dashboard.cerebrium.ai since we will need to get our API keys to deploy this example.
3. Run the following command in your terminal: `pip install --upgrade cerebrium``.
4. Run the following command in your terminal: `cerebrium login <private_api_key>``. The private-api_key can be found on your Cerebrium dashboard.
5. Run the command cerebrium deploy pet-detection --config-file ./config.yaml
6. Your deployment will take about a minute or 2 since we are setting up your environment. Don't worry, subsequent deployments will be much faster if you make changes:)

Congrats your deployment should be live and you should see it live in your dashboard. You then should see a Curl Request in your terminal or example requests in your dashboard which we will use in the steps below to call our implementation.

## Using Pet Detector
This Pet detector example joins your call as a bot, silently monitoring every video on your call. In order to get it to join a Daily call, you need to send it the video
url you want it to join. This is done doing something similar to:

```bash
curl --location --request POST 'https://run.cerebrium.ai/v3/p-xxxx/pet-detection/predict' \
--header 'Authorization: <JWT_TOKEN>' \
--header 'Content-Type: application/json' \
--data '{"room": "Your Daily Room URL"}'
```

## Questions/Feedback
In order to give feedback to the Daily or Cerebrium teams please reach out to:
- Daily: support@daily.co
- Cerebrium support@cerebrium.ai