# Cloud Passport: SAA-C03 practice app

Built from the design and study logic of your Studiepass (medborgarskapsprovet) app.

## Windows
Double-click `CloudPassport.html`. It opens in your browser and works offline.
Progress is saved in that browser. Use the same browser each time.

## iPhone
The `iphone-web-app` folder has to be opened once from a web address. Then:
1. Open the address in **Safari**.
2. Tap Share, then **Add to Home Screen**.
3. Open it once from the home screen. After that it works offline.

## Moving progress between PC and phone
Data tab > Export on one device, then Import on the other. Import replaces progress on that device.

## What is inside
- 297 practice questions in 13 chapters, each with an explanation, plus a cheat sheet per chapter.
- Practice: the answer and explanation appear right after you answer.
- Smart repetition: wrong answers come back the same day; right answers come back after 1, 3, 7, 14 and 30 days.
- Mock exam: 65 questions, 130 minutes, flag and jump between questions, estimated score against 720.
- Half exam (30 questions / 60 min), Quick 15 weak spots, Mixed 50.
- Stats: estimated score, weakest chapters, last 7 days, exam history.

## Credits
Questions and cheat sheets: https://github.com/ChathurangaVKD/AWS-Certified-Solutions-Architect-Associate-SAA-C03
MIT License, Copyright (c) 2025 AWS Solution Architect Study Guide Contributors.
These are original practice questions, not real exam questions. Scores are estimates.

## Rebuilding
`source/parse.py <question-repo> data.js` turns the question repo into data, then `source/build.py <out> data.js` builds both versions.
The iPhone version is served by GitHub Pages from this repo's root.
