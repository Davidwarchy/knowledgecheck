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

The dic is by wordnet

### Prerequisites
1. Python https://www.python.org/downloads/ 

### Warnings
1. The project installs dependencies automatically.
2. This has been tested only on windows and may break on linux

### Clone or download the project
#### Clone
https://github.com/Davidwarchy/knowledgecheck.git

### Run 
```py .\run.py```

Output for the process ought to resemble this:

![image](https://github.com/Davidwarchy/knowledgecheck/assets/17954362/3f7f5e72-7c7d-474d-931a-6694314ba412)

### View entities in our local knowledge graph
You can run this command to check the entities in our local knowledge graph currently. 

```py .\lkg.py```

