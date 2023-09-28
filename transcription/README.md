# Transcription Demo

## Description

This repository contains code for the transcription demo project using Daily and Cerebrium. In this example, we have a bot that monitors the entire conversation of a call across each participants and once the call ends, transcribes it using the OpenAI Whisper model and sends a transcription of the call to the email address you define. 

## Setup
In this example we have two deployments to make. A CPU based deployment and a GPU based deployment. The reason for this is due to the fact that GPU deployments are expensive to constantly run so we use a CPU deployment to constantly monitor the audio of the call. Once the call ends, it sends the audio file to the GPU based deployment to do the transcription. Typically 13 minutes of audio takes about 54s to transcribe.


## Deployment Instructions
You can deploy the example below in just a few easy steps.
1. Git clone the repository and make sure you are in the transcription/MonitorAudio or transcription/WhisperModel folder
2. Sign up at https://dashboard.cerebrium.ai since we will need to get our API keys to deploy this example.
3. Run the following command in your terminal: `pip install --upgrade cerebrium``.
4. Run the following command in your terminal: `cerebrium login <private_api_key>``. The private-api_key can be found on your Cerebrium dashboard.
5. Run the command cerebrium deploy --config-file ./config.yaml in each of the two folders.
6. Your deployment will take about a minute or 2 since we are setting up your environment. Don't worry, subsequent deployments will be much faster if you make changes:)

Congrats your deployment should be live and you should see it live in your dashboard. You then should see a Curl Request in your terminal or example requests in your dashboard which we will use in the steps below to call our implementation.

## Using Transcription bot
This transcription example joins your call as a bot, silently monitoring everything that is said on a call. In order to get it to join a Daily call, you need to send it the video url you want it to join and the email address you want it to send the deployment to afterwards. This is done doing something similar to:

```python

```

## Questions/Feedback
In order to give feedback to the Daily or Cerebrium teams please reach out to:
- Daily: support@daily.co
- Cerebrium support@cerebrium.ai