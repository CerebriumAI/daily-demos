# Content Moderation Demo

## Description

This repository contains code for the a content moderation demo project using Daily and Cerebrium. In this example, we have a bot that monitors each participants screen
for a set of classes that we can define such as weapons, drugs, nudity etc using a CLIP model. If one of those classes is detected above 70% then a message broadcast is sent to all participants which you can decide what to do with. We then have a custom made UI in React that renders which participant is commiting the offense. 

## Deployment Instructions
1. First deploy your moderator-client which, if running locally, will create a room on your Daily account. You can follow the README.md in this folder to deploy this.
2. Deploy your moderator-model to Cerebrium and then get it to join the room create in step 1 in order to moderate the content. You can follow the README.md in the folder.

## Questions/Feedback
In order to give feedback to the Daily or Cerebrium teams please reach out to:
- Daily: support@daily.co
- Cerebrium support@cerebrium.ai