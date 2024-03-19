# Neural Decoding - PharmaHacks2024

Welcome to our teams' repository for McGill's PharmaHacks Neural Decoding challenge! If you are interested in viewing our code, you can click [here](./PharmaHacks 2024 Neural Decoding Single File.ipynb)

## 🏬 Our Team 
> Hyperlinks lead to LinkedIn profiles*
-  **[Marcus Lee](https://www.linkedin.com/in/marcus-lee-3b5298264/)** DEC, Computer Science & Math @ Vanier College 💻
-  **[Carson Spriggs-Audet](https://www.linkedin.com/in/carson-spriggs-audet-609372217/)** DEC, Computer Science @ John Abbott College 💻
-  **[Jiwon Kim](https://www.linkedin.com/in/jiwon-kim-32b39a261/)** BS, Life Science | Brain & Cognivitive Science @ Korea University 🧠
-  **[Seungyeon Lee](https://www.linkedin.com/in/seungyeon-lee/)** BS, Neuroscience, Minor in Computer Science @ McGill 🧠
-  **[Amélie Beaudin](https://www.linkedin.com/in/am%C3%A9lie-beaudin-60241b248/)** BS, Computer Science @ McGill 💻

## ⭐ PharmaHacks

[PharmaHacks](https://www.linkedin.com/company/pharmahacks/) is a hackathon organized by students of McGill University. PharmaHacks' mission is to "provide interested students with bioinformatics/cheminformatics training through extracurricular means to prepare them for future jobs in industry, academia, and government."[^1]

We want to thank the organizers for putting together such an amazing event, we look forward to future events!

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
