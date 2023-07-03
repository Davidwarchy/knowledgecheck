# Knowledgecheck - A Sequence For Entity Checking from a Phrase  
I think that there are a few components involved while looking up a phrase.
1. Local KG check
2. Foreign KG check
3. Dictionary Check
4. Trimming the phrase 

### Sequence
![image](https://github.com/Davidwarchy/knowledgecheck/assets/17954362/c0de34cd-1d18-4c98-a25c-6bf069b14dd3)

The local is a simple table listing names of entities 

The foreign kg is check is done with a query to https://lookup.dbpedia.org/

The dic is by wordnet https://wordnet.princeton.edu/

### Prerequisites
1. Python https://www.python.org/downloads/
2. Pip (add pip to system path) - most versions of python do this automatically. \
Run ```pip``` on the command prompt to see if it's installed

### Warnings
1. The project installs dependencies automatically if prerequisites are installed well.
2. This has been tested only on windows and may break on linux

### Clone or download the project
#### Clone
https://github.com/Davidwarchy/knowledgecheck.git

OR
#### Download & Unzip 
<img width="316" alt="image" src="https://github.com/Davidwarchy/knowledgecheck/assets/17954362/bd5de2fc-01ea-4f23-837b-f5ce59e72c12">

### Run 
```py .\run.py```

Output for the process ought to resemble this:

![image](https://github.com/Davidwarchy/knowledgecheck/assets/17954362/3f7f5e72-7c7d-474d-931a-6694314ba412)

### View entities in our local knowledge graph
You can run this command to check the entities in our local knowledge graph currently. 

```py .\lkg.py```

