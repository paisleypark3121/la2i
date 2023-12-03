---
title: Chainlit Docker
emoji: 📉
colorFrom: yellow
colorTo: red
sdk: docker
pinned: false
---

ABOVE SECTION IS FOR DOCKER: it must be the first instruction in the readme.md file

---

Start chainlit: chainlit run app.py -w

Please create an .env file and insert your openai api key:
OPENAI_API_KEY=**USE YOUR KEY**

Hide the chain of thought details from the user in the UI:
hide_cot = false

---

in order to generate automatically the requirements.txt file: 
OPTION1: pipreqs (pip install pipreqs) and then use the command: pipreqs . --force
OPTION2: pip freeze > requirements.txt

--- 

CHAINLIT AUTHENTICATION
In ordero to handle Chainlit authentication it is necessary to generate a Chainlit key:
chainlit create-secret
This command generates a key that has to be inserted in the .env file
(BEWARE: it is necessary that the KEY doesn't contain strane patterns as = in the middle; you recognize that it is correct in .env file in VSCODE because CHAINLIT_AUTH_SECRET is blue and its value is ALL WHITE)
It is necessary to insert the default ACCESS username and password:
LA2I_USERNAME=**USE YOUR KEY**
LA2I_PASSWORD=**USE YOUR KEY**

---

TUTORIAL - DEPLOY ON HUGGINGFACE SPACE

1. Create the Dockerfile: see Dockerfile file

2. Create a new space in HuggingSpace with deploy option Docker

3. Create access token in HuggingFace: settings -> access tokens -> create a new token in WRITE mode

4. Github secret: in Github repo -> settings -> secret and variables -> actions -> new repo secret
create the HF_TOKEN with the value of the token configured in HuggingFace

5. Create the .github/workflows/ directory to store your workflow files:
- actions_onpull.yaml
- actions_onpush.yaml

6. set origin: git remote set-url origin https://GITHUB_USERNAME:HF_TOKEN@huggingface.co/spaces/HF_USER/HF_SPACE_NA;E

7. git pull origin


