# Group 16 DSA3101 Project
Our group's project is about conducting sentiment analysis on online reviews of GXS' mobile app on the Google Play Store and Apple App Store. 

## Docker 
The directory for Backend's dockerfile is:
```
Backend
```

The directory for Frontend's dockerfile is:
```
Frontend
```

The docker compose file is in the main directory.
To use our application, please change the OPENAI_API_KEY in the file 'constants' and run 
```
docker compose up --build -d
```
in the root folder. Then you can use our application on 
```
http://localhost:8050/
```
The OPENAI_API_KEY is in the Technical Report file, at the end of part 6 ChatGPT API.
