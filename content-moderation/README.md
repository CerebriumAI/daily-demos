# Content Moderation Demo

## Description

This repository contains code for the a content moderation demo project using Daily and Cerebrium. In this example, we have a bot that monitors each participants screen
for a set of classes that we can define such as weapons, drugs, nudity etc using a CLIP model. If one of those classes is detected above 70% then a message broadcast is sent to all participants which you can decide what to do with.

## Deployment Instructions
You can deploy the example below in just a few easy steps.
1. Git Clone the repository and make sure you are in the content-moderation folder
2. Sign up at https://dashboard.cerebrium.ai since we will need to get our API keys to deploy this example.
3. Run the following command in your terminal: `pip install --upgrade cerebrium``.
4. Run the following command in your terminal: `cerebrium login <private_api_key>``. The private-api_key can be found on your Cerebrium dashboard.
5. Run the command cerebrium deploy --config-file ./config.yaml
6. Your deployment will take about a minute or 2 since we are setting up your environment. Don't worry, subsequent deployments will be much faster if you make changes:)

Congrats your deployment should be live and you should see it live in your dashboard. You then should see a CURL Request in your terminal or example requests in your dashboard which we will use in the steps below to call our implementation.

## Using Content Moderator
This Content Moderator example joins your call as a bot, silently monitoring every video on your call. In order to get it to join a Daily call, you need to send it the video url you want it to join. This is done doing something similar to:

```python

```

## Questions/Feedback
In order to give feedback to the Daily or Cerebrium teams please reach out to:
- Daily: support@daily.co
- Cerebrium support@cerebrium.ai