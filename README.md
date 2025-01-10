
<h1 align="center">
  <br>
  <a href=""><img src="img/logo.jpeg" alt="logo" width="200"></a>
  <br>
  multi modal ai product showroom 🤖
  <br>
</h1>

<h4 align="center">A minimal speech-to-structured output app built with Azure OpenAI Realtime API.</h4>
</p>


## Problem we are addressing

- **Documentation overhead**: dealing with high volumes of documents and having at the same time not enough time in the day to maintain/fill them in;
- **Information loss**: if it takes a document or a form too long to be filled - information will get lost!


## Key features and technical details

![screenshot](img/screenshot.png)

- Backend: python
- Frontend: minimal JS, CSS/HTML

The app has minimal dependencies to allow for easy extension and integration with other communication channels and applications.

## Architecture

![architecture](img/architecture.png)
## How to set up the Azure environment

To run this application, you can provision the resources using azure developer CLI.

From your command line:

```bash
echo "log into azure dev cli - only once"
azd auth login

echo "provisioning all the resources with the azure dev cli"
azd up

# The following values should work:
# location=northeurope
# aiResourceLocation=swedencentral

echo "get and set the value for AZURE_ENV_NAME"
source <(azd env get-values | grep AZURE_ENV_NAME)

echo "building and deploying the streamlit user interface"
bash ./azd-hooks/deploy.sh app $AZURE_ENV_NAME
```

> **Note**
> If you do not provision a cosmosDB, you can still run the app using the local sample files. To replace the data source, substitute the cosmosdb module.


## Flow

AI: Welcome. We have X available. What are you interested in?
User: I am interested in fridge

AI: We have x models available. Notable difference between the models are number of compartments, 



## Disclaimer

This is an open-source repository and it does not have official support from Microsoft. Use at your own risk 😉

For production scenarious, questions and bugs please open a Github issue.
