# Hacktoberfest @ IE


## Setup [Open Interpreter](https://docs.openinterpreter.com/introduction)
To make the experience of using git much easier for you during our workshops, we chose to use open-interpreter to help guide you thought your learning journey of using git.

To install open-interpreter you will need the [latest stable version](https://www.python.org/downloads/) of [Python](https://www.python.org/downloads/) and secondly you will need to [install pip](https://pip.pypa.io/en/stable/installation/)

### What is Open Interpreter
Open Interpreter is a free, open-source tool that facilitates the execution of code on your computer, harnessing the capabilities of language models.

### Installation
+ [ ] Install Python 3.6 or higher
+ [ ] Install pip

Now you can install Open Interpreter using pip:
```bash
pip install open-interpreter
```

Now you will need to get an API key from OpenAI at this [link](https://platform.openai.com/account/api-keys).


![demo](https://static1.howtogeekimages.com/wordpress/wp-content/uploads/2023/04/red-arrow-pointing-to-the-button-that-generates-a-new-API-key.jpg?q=50&fit=crop&w=750&dpr=1.5)

1. Click on the "Create New Secret Key" button
2. Give your key a name _(e.g. open-interpreter)_
3. Copy the key and run the following command in your terminal:


for Linux/MacOS:
```bash
export OPENAI_API_KEY=<your-api-key>
```

for Windows:
```bash
set OPENAI_API_KEY=<your-api-key>
```

### Usage
Once installed, you can launch Open Interpreter by running the `interpreter` command in your terminal. This will open up a natural-language interface allowing you to communicate with your computer and execute code seamlessly.

Congratulations! You are now ready to use Open Interpreter :tada: :tada: :tada:


## How to contribute
This guide will provide you with a set of resources and questions you can ask open-interpreter to help you get started with contributing to open source projects.

1. We made a repository for you to practice contributing to open source projects. You can find it [here](https://github.com/haxybaxy/testrepo). To contribute to this repository you will need to fork it first. You can do that by clicking on the fork button on the top right corner of the repository page.

2. Now you will need to clone the repository to your local machine. You can do that by clicking on the green code button and copying the link. Now is time to go to your terminal running open-interpreter, paste in the link and ask it to clone the repository for you. Ex:

> Hey! I have a forked repository on github. I want to clone it to my local machine. Can you help me with that? The link to the repository is: https://github.com/velocitatem/hacktobertest

3. Now that you have the repository on your local machine, you can start making changes to it. We start making changes by creating a new branch. You can do that by asking open-interpreter to create a new branch for you. Ex:

> Now that I have the repository on my local machine, I want to create a new branch. Can you help me with that? The name of the branch should be: <my-new-branch>

4. Now that you have a new branch, you can start making changes to the repository. You can do that by asking open-interpreter to create a new file for you or open the project in your favorite code editor. Ex:

> I now need to create a new file. Can you help me with that? Please open the main python file in my favorite code editor. My favorite code editor is: vscode

5. Now that you have made some changes to the repository, you can ask open-interpreter to help you commit and push your changes to your forked repository. Ex:

> I have made some changes to the repository. Can you help me commit and push them to my forked repository? The commit message should be: <my first commit>

6. Now that you have pushed your changes to your forked repository, you can ask open-interpreter to help you create a pull request to the original repository. Ex:

> I have pushed my changes to my forked repository. Can you help me create a pull request to the original repository? Please open the pull request in my browser.

Congratulations! You have successfully contributed to an open source project :tada: :tada: :tada:


# Additional Resources
+ [CodeRabbit](https://coderabbit.ai/)
+ [Github Copilot](https://github.com/features/copilot)
+ [Interactive Github Lab](https://skills.github.com/)
+ [AI Commits](https://github.com/Nutlope/aicommits)
