<p align="center">
  <img src="https://img.icons8.com/external-tal-revivo-regular-tal-revivo/96/external-readme-is-a-easy-to-build-a-developer-hub-that-adapts-to-the-user-logo-regular-tal-revivo.png" width="100" />
</p>
<p align="center">
    <h1 align="center">PRD TO User Stories</h1>
</p>
<p align="center">
    <em>Transforming Ideas into Action: PRD to User Stories</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/ulfimlg/PRD_to_UserStories?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/ulfimlg/PRD_to_UserStories?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/ulfimlg/PRD_to_UserStories?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/ulfimlg/PRD_to_UserStories?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=Streamlit&logoColor=white" alt="Streamlit">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
</p>
<hr>

##  Quick Links

> - [ Overview](#-overview)
> - [ Features](#-features)
> - [ Repository Structure](#-repository-structure)
> - [ Modules](#-modules)
> - [ Getting Started](#-getting-started)
>   - [ Installation](#-installation)
>   - [ Running PRD_to_UserStories](#-running-PRD_to_UserStories)
> - [ Contributing](#-contributing)
> - [ License](#-license)
> - [ Acknowledgments](#-acknowledgments)

---

##  Overview

This project converts PRD into well defined user stories with the help of Microsoft Autogen orchestration. It provides a comprehensive breakdown of each requirement by scanning through the PDF and simplifying the requirements into Epics, Features then User stories sequentially. The final Output of each layer is provided to the user and the output is integrated with Jira, a Project Management Platform, where the team can start managing sprints and work with the user stories on the go!

---

##  Features

The features provided by this project are:
- Comprehensive Epic creation
- Features with well defined sub tasks,
- Detailed User stories with acceptance criteria
- Integration with Jira

---

##  Repository Structure

```sh
└── PRD_to_UserStories/
    ├── LICENSE
    ├── README.md
    ├── app.py
    ├── epic_feature.py
    ├── feature_user.py
    ├── prd_epic.py
    └── requirements.txt
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                           | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---                                                                                            | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [feature_user.py](https://github.com/ulfimlg/PRD_to_UserStories/blob/master/feature_user.py)   | The `feature_user.py` script within the `PRD_to_UserStories`repository is primarily intended to use AI agents to convert features into detailed, refined user stories, adhering to SMART criteria. The script also helps maintain alignment with the overarching product vision, embodying the responsibilities of a product owner in an Agile setting.                                                                                                                                                    |
| [epic_feature.py](https://github.com/ulfimlg/PRD_to_UserStories/blob/master/epic_feature.py)   | This script, `epic_feature.py`, is a component of the `PRD_to_UserStories` repository that is responsible for converting product requirements (epics) into tangible features. By using AI-driven agents, the script emulates the role of a product owner, breaking down epics and refining the output based on team feedback and technical constraints. It neatly fits into the repository's goal of automating product requirement management.                                                         |
| [prd_epic.py](https://github.com/ulfimlg/PRD_to_UserStories/blob/master/prd_epic.py)           | The `prd_epic.py` snippet is fundamental in converting Product Requirement Documents into epics. The file incorporates AssistantAgent and UserProxyAgent to facilitate the process, preventing direct human input. The code constructs an interactive environment where an AI-driven Product Manager breaks down PRDs into several epics, involving other AI agents for definition and refinement suggestions. This streamlined approach helps in efficient PRD dissection and delivery of refined epics. |
| [requirements.txt](https://github.com/ulfimlg/PRD_to_UserStories/blob/master/requirements.txt) | This codebase is primarily for transforming Product Requirement Documents (PRDs) to User Stories. The `requirements.txt` file lists dependencies that provide functionalities such as automatic code generation, PDF processing, environment management, and machine learning experimentation. The architecture implements the conversion process in a modular way by structuring separate functions into files such as `app.py`, `prd_epic.py`, `epic_feature.py`, and `feature_user.py`.              |
| [app.py](https://github.com/ulfimlg/PRD_to_UserStories/blob/master/app.py)                     | This code in `app.py` serves as the core application interface in the `PRD_to_UserStories` repository. It imports other module functions such as PRD to epic conversion, epic to feature conversion, and feature to user story conversion. Additionally, the code enables environment setup, access to a specified API with authentication, and media extraction from documents, contributing to the central functionality of translating Product Requirement Documents into user stories.                  |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version 3.11.5`

###  Installation

1. Clone the PRD_to_UserStories repository:

```sh
git clone https://github.com/ulfimlg/PRD_to_UserStories
```

2. Change to the project directory:

```sh
cd PRD_to_UserStories
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```
4. Create a `.env` file with:
```
LANGTRACE_API_KEY=<api_token>
```
5. Create a `OAI_CONFIG_LIST.json` file with:
```
[{
    "model":"<model_name>",
    "api_key":<api_token>
}]
```
6. Set domain for your Jira in `app.py`:
```
#Fill in your domain url before running

url  =  "https://your-domain.atlassian.net/rest/api/3/issue"
```
7. Set your API and Email for Jira in  `app.py`:
```
#Enter your personal email and your API key here

auth  =  HTTPBasicAuth("email@example.com", "<api_token>")
```
8. Update the `post_jira()` function in   `app.py`:
```
#Function which sends each User story to Jira (Before running update "key": The key of your project)(Also update "issuetype": the number shown on Jira issue filter)
def  post_jira(story,user_no):
	"issuetype": {
	"id": "10001"#Update
	},
	"project": {
	"key": "AT"#Update
	},
```

###  Running PRD_to_UserStories

Use the following command to run PRD_to_UserStories:

```sh
streamlit run app.py
```
---


##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/ulfimlg/PRD_to_UserStories/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/ulfimlg/PRD_to_UserStories/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/ulfimlg/PRD_to_UserStories/issues)**: Submit bugs found or log feature requests for Prd_to_userstories.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/ulfimlg/PRD_to_UserStories
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [MIT LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---


[**Return**](#-quick-links)

---
