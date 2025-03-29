# IBM Challenge - Group 11
Welcome to the home of the Solution for the IBM-Challenge 2025. 👋

## Table of Contents
1. [About the Project](#about-the-project)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration](#configuration) _(if applicable)_
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## About the Project
This project is about using any LLM provided by watsonX to compare initial NDAs. The LLM shoul be able to find not needed or really restrictive sentences in a word document. Furthermore, it should highlight/comment those parts of the document and present it to an internal SME. After the review of the SME the document should be transformed into its final format and stored to be ready to sent to the other party. 

## Features
- ✅ Read Word-Document and upload to watsonX
- ✅ Generate comments for not needed texts wit LLM 
- ✅ Present LLM suggestions to internal SME to review
- ✅ Transform document into PDF to be ready to ship

## Installation
**Pyton-Setup:** 
1. Make sure to install Python version between ``` 3.10 and 3.12!! ```
2. Install the packages from requirements.txt with ``` pip install -r requirements.txt```

**Project-Setup:**
1. Clone this repository
2. Create a ``` .env ``` file in the same folder
3. Download a example NDA from box.com
4. Add the following variables to the ``` .env ``` file:
``` ENV
APIKEY = xxxxxxxxxxx
PROJECTID = xxxxxxxxxxx
SPACEID = xxxxxxxxxxx
IBMLOCATION = https://eu-de.ml.cloud.ibm.com
```

## Usage
1. Change imported filename to ``` nda.docx ```
3. Run ```exploreWatsonX.ipynb``` inside vscode or any other editor using jupyter-notebooks extension. 

## Configuration

## Contributing

## License

## Contact