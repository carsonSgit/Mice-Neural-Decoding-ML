# Neural Decoding - PharmaHacks2024

Welcome to our teams' repository for McGill's PharmaHacks Neural Decoding challenge! If you are interested in viewing our code, you can click [here](./PharmaHacks%202024%20Neural%20Decoding%20Single%20File.ipynb)

## 🏬 Our Team 
> Hyperlinks lead to LinkedIn profiles*
-  **[Marcus Lee](https://www.linkedin.com/in/marcus-lee-3b5298264/)** DEC, Computer Science & Math @ Vanier College 💻
-  **[Carson Spriggs-Audet](https://www.linkedin.com/in/carson-spriggs-audet-609372217/)** DEC, Computer Science @ John Abbott College 💻
-  **[Jiwon Kim](https://www.linkedin.com/in/jiwon-kim-32b39a261/)** BS, Life Science | Brain & Cognivitive Science @ Korea University 🧠
-  **[Seungyeon Lee](https://www.linkedin.com/in/seungyeon-lee/)** BS, Neuroscience, Minor in Computer Science @ McGill 🧠
-  **[Amélie Beaudin](https://www.linkedin.com/in/am%C3%A9lie-beaudin-60241b248/)** BS, Computer Science @ McGill 💻

## ⭐ PharmaHacks

[PharmaHacks](https://www.linkedin.com/company/pharmahacks/) is a hackathon organized by students of McGill University. PharmaHacks' mission is to "provide interested students with bioinformatics/cheminformatics training through extracurricular means to prepare them for future jobs in industry, academia, and government."[^1]

We want to thank the [organizers](https://pharmahacks.com/Team) for putting together such an amazing event, we look forward to future events!

>[!NOTE]
>PharmaHacks 2024 had two challenges;
> - **Neural Decoding:** From Calcium Imaging Data, analyze and predict results from neural activity.
> - **Genomics:** Using scRNA-seq data, predict Covid-19 case severity in patients



[^1]: [PharmaHacks' LinkedIn](https://www.linkedin.com/company/pharmahacks/)

## :label: Problem Description

**Neuroscientist & Dr. [Shih-Yi Tseng](https://www.linkedin.com/in/shih-yi-tseng/) et al.** published a [Neuron paper](https://www.cell.com/neuron/fulltext/S0896-6273(22)00453-6?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS0896627322004536%3Fshowall%3Dtrue) documenting their experiments performed on 8 mice. The experiment captures over 200,000 neurons over 6 areas of the mices' posterior cortices; L2/3 and L5, V1, secondary visual areas, Retrosplenial Cortex (RSC), and the Posterior Parietal Cortext (PPC).

![image](https://github.com/GodPuffin/Pharmahacks2024/assets/92652800/544abb7a-615f-4bdb-a226-fa71bf0a38e8)
###### *Image source: Tseng, Shih-Yi, et al. “Shared and specialized coding across posterior cortical areas for dynamic navigation decisions.” Neuron, vol. 110, no. 15, Aug. 2022, https://doi.org/10.1016/j.neuron.2022.05.012.*
> The mice are given two possibilities, **black** walls or white walls. The correct choice of turning is according to two rules.
>> **Rule A:** the mice must turn **left** when the walls are **black** and **right** when the walls are **white**.
>> 
>> **Rule B:** the mice must turn **right** when the walls are **black** and **left** when the walls are **white**.

<br />

![image](https://github.com/GodPuffin/Pharmahacks2024/assets/92652800/4b7fac34-1043-4a85-8155-b0442ff2bd58)
###### *Image source: Tseng, Shih-Yi, et al. “Shared and specialized coding across posterior cortical areas for dynamic navigation decisions.” Neuron, vol. 110, no. 15, Aug. 2022, https://doi.org/10.1016/j.neuron.2022.05.012.*
> The maze the mice were trialed in is shown above.
>
> It is a Y-shaped maze with two choices, **left** or **right**. After they make their turn, they are looped back to the beginning of the maze & trialed again (approx. 400 trials per day of experimenting).

<br />

Thanks to their experiment, we are able to access the mices' neural data and analyze what neuron activation corresponds to navigation decision making. 

From the [data provided](https://dandiarchive.org/dandiset/000579) by the researchers, we were tasked with creating a Machine Learning model that would be able to predict a mouse's position in the maze.


## Problem Approach

#### Analysis 

Our first mission was to understand the data. after thorough research & analysis of the neural paper & use tutorial of the data, we narrowed down our focus to these specific factors:
- **The RSC:** We chose to isolate our focus on the RSC due to it's functions encompassing navigation and spacial memory. 
- **The L2/3 neurons:** Our data presented us with the L2/3 layers & the L5 in separate files. We decided on working with the L2/3 due to it's relations in processing sensory information. 
- **Multi-plane images:** Having been given the option between Single-Plane & Multi-Plane imaging, we chose to go with Multi-Plane so that we had more comprehensive data to work with. 


#### Data processing

The data has 4 deconvoluted planes, each of which are desynchronized from one another & have many NaN (missing) values. Below was our process to resolve these issues;

- **Unsynchronized data:** 
    - [x] Join all **4 deconvoluted planes** together. 
    - [x] Format the columns to accurately reference to the Timestamp data (Timestamp of neuron activity capture). 
    - [ ] 

- **NaN values:** Two methods of resolution
    - [x] Dropped all NaNs and saved in a new set. 
    - [x] Utilized an IterativeImputer model to impute what the missing data should be according to it's surrounding data values. 

#### Machine Learning Model

Once it came down to choosing a model, we had to research different categories of models. Through our prior analysis, we knew we wanted to use something of the classification/regression sort which led us to using a **RandomForestRegressor**. 

> What is a **RandomForestRegressor**?
>> To explain this, first we have to look at what a **DecisionTreeRegressor** is. 
>> A DecisionTreeRegressor is a model that recursively splits the training data into partitions. 
>> These splits allow for the model to choose which data best fits the training data & predicts off of the most accurate splits (leafs). 
> So what *is* a **RandomForestRegressor**?
> A RandomForestRegressor creates & trains multiple *DecisionTreeRegressors* on subsets of the data. It then chooses the DecisionTreeRegressors with the lowest error indicators & averages them together to create the most accurate possible version. 