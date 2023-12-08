[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/NxMd-3_v)
# CMU Interactive Data Science Final Project - Magic Magician

* **Team members**:
  * Contact person: mingxinl@andrew.cmu.edu
  * yitianx2@andrew.cmu.edu
  * ndhanase@andrew.cmu.edu
  * epguo@andrew.cmu.edu
  
### Summary Image (Gif)

![Gif - Step 3](./assets/04-final-summary.gif)

## Abstract
The data science problem addressed in this project is the exploration and understanding
of the evolution of music over time using a curated dataset from the Interdisciplinary
Contest in Modeling (ICM) for Problem D in 2021. The dataset encompasses various
characteristics of music, such as acousticness, energy, instrumentalness, loudness,
tempo, explicitness, and frequency of musical keys, among others. The objective is
to gain insights into music trends, artist characteristics, and the influence of
past music on new compositions.

The Streamlit application developed for this purpose consists of four main sections:
Data by Year, Data by Artist, Data by Song, and Music Influence. In the Data by Year
section, informative visualizations are presented to highlight trends and changes
in music characteristics over different decades, accompanied by explanations of
significant events influencing these trends. The Data by Artists section provides a
characteristic overview of each artist, allows comparison between artists, and
ranks artists by greatest and smallest popularity. The Data by Song section allows users
to explore the dataset comprehensively through three tabs, offering an overview of
the dataset, ranking songs based on popularity, and comparing individual songs across
various attributes. The Music Influence section delves into influencer-follower
relationships among artists, employing innovative techniques such as the "pivot-melt"
approach for constructing stacked distribution charts and incorporating interactive
network visualizations.

Our solution effectively addresses the problem by providing a user-friendly interface
that facilitates in-depth exploration of the dataset, enabling users to uncover patterns,
correlations, and influential factors in the realm of music. The incorporation of
diverse visualizations and interactivity enhances the user experience and contributes
to a comprehensive understanding of the multifaceted aspects of music over time.

## Installation
### Prerequisites
- Python environment with 3.8 or above
- Package manager such as pip or conda that allows you to download dependencies

### Install
1. Clone this repo using: ```git clone git@github.com:CMU-IDS-Fall-2023/final-project-musicmagicians.git```
2. In your local environment:
    1. If you use conda, run ```conda install --file requirements.txt```; 
    2. If you use pip, run ```pip install -r requirements.txt```
3. To run the application:
    1. Run ```streamlit run Spotify_Music_Data_Overview.py```
    2. If the above does not work, try ```python -m streamlit run Spotify_Music_Data_Overview.py```

## Work distribution
- Intro page      : Equal contributions
- Data by Year    : Emily Guo epguo@andrew.cmu.edu
- Data by Artist  : Nivedhitha Dhanasekaran ndhanase@andrew.cmu.edu
- Data by Songs   : Mingxin Li mingxinl@andrew.cmu.edu
- Artist Influence: Yitian Xu yitianx2@andrew.cmu.edu

## Deliverables

* **Video**: [Demonstration](https://youtu.be/5e2C-uLXFgs)
* **Report**: [Project report Markdown](Report.md)
* **Proposal**: [Project proposal Markdown](Proposal.md)
* **Proposal**: [Project Proposal Google Drive](https://docs.google.com/document/d/12_InTimLdOuIm3lGfAHxmgSYuEV3K-SWiDrrchgJ_KY/edit?usp=sharing)

The team regularly met to discuss, plan, and develop the design for the application. After splitting the workload, each member independently developed their components. Lastly, bugs were collaboratively fixed, and documentation was collectively prepared.

### Proposal

- [x] The URL at the top of this readme needs to point to your application online. It should also list the names of the team members.
- [x] A completed [proposal](Proposal.md). Each student should submit the URL that points to this file in their GitHub repo on Canvas.

### Sketches

- [x] Develop sketches/prototype of your project.

### Final deliverables

- [x] All code for the project should be in the repo.
- [ ] ~~Update the **Online URL** above to point to your deployed project.~~
- [x] A detailed [project report](Report.md).  Each student should submit the URL that points to this file in their github repo on Canvas.
- [x] A 5 minute video demonstration.  Upload the video to this github repo and link to it from your report.
