# Generate Vanity Number
mainfile.py is the file that gets invoked when calls are made to Amazon Connect number.
In this code, phone number customer is calling from is considered as input and five Vanity options are returned. These five are added to DynamoDB along with phone number.
Three options are returned to customers on call.

This code can be updated to use a manual input number rather than just calling number as input by setting a contact attribute and by passing it to Lambda.
Requirement was to return five best results among Vanity, but that task is not complete.

CloudFormation template is added to the repository which generates stack that includes Lambda functions, Layers, and DynamoDB to store the Vanity number details.
Custom resource to create call flow and automatically associate Lambda function is not added to the CF template.
CF template can be updated to refine roles and policies rather than using managed policies in order to restrict access.

To determine Vanity options code from Srinivasnac's code from GitHub is referenced and used. Below are the details about the Vanity Generator algorithm,

A [vanity number]((https://en.wikipedia.org/wiki/Vanity_number)) is a local or toll-free telephone number for which a subscriber requests an easily remembered sequence of numbers for marketing purposes. For example, '1-866-386-6481' => '1-866-FUNMIT1'

This is a Python Module implementing functionalities related to [Vanity Toll-free Phone Numbers](https://en.wikipedia.org/wiki/Vanity_number), like wordification generation, Number mapping, validation, etc. For example:
- `Number to word Generation`: the Toll Free Number "1-800-724-6837" could be wordified to "1-800-PAINTER" for remembering easily, and there could be other wordifications.
- `Word to number mapping`: The telephone number corresponding to the wordified number '1-866-FUNMIT1' is '1-866-386-6481'
- `Phone Number validation`: '404739-92' and '6504939270' are NOT valid US Phone Numbers.


##  Approach and Algorithm used

Main files are [wordify.py] and [helper.py]

[`all_wordifications`] Given a valid Toll-free Number (e.g.`"1-800-724-6837"`), we would like to generate and return various possible Vanity Numbers (e.g.[`"1-800-PAINTER"`, ...]), which are valid word combinations. This problem of generating valid word combinations of a phone number is approached by considering it as a graph problem, with Nodes called `T9_Graph_Node` representing possible combinations of characters for each of the digit, and Breadth first search is performed from the first digit, till the end of the number. [Comparator operators](https://softwareengineering.stackexchange.com/a/151075) has been over-ridden for `T9_Graph_Node` for performing custom comparison operations between Graph Nodes, during operations like sorting, min, max, etc.

While doing graph search, since it is required to frequently check if the prefix word is a valid dictionary word, [Trie Data structure](https://en.wikipedia.org/wiki/Trie) is Used. To populate the Trie, Dictionaries.txt is read and Trie Data Structure has been created and saved in a global variable. Python Dictionary type could also have been used for checking for a valid dictionary word, but it will Be more memory intensive to store all dictionary words in local memory while the program is running, and the program may crash for larger number of dictionary entries. Trie data structure can support much larger dictionary sizes.

The List of possible outputs are stored in Max Heap / Priority Queue for faster insertion and deletion queries and retrieving best N words, which is defined by comparator function (most number of English characters in wordified_number)

[Graph Search (BFS)] : For performing graph search, [BFS](https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/) is used, which is more intuitive to this problem that [DFS](https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/)

Number Validation: Since US phone numbers can come in slightly different formats (1-800-724-6837, 4046639270, 404-663-9270, 1-(866)-(724)-(6836), etc ) and to validate them handling these cases, [Regular Expressions](https://www.regular-expressions.info/) is used to validate, as well as compare phone numbers and fetch groups of area codes. Though sometimes it is recommended to avoid Regex, this usecase of fetching US phone number area codes looked more suitable for its use, to avoid writing complex and repeating logic for validating, matching and fetching groups of numbers in the US phone number, Regular expression approach is used.

[`number_to_words`]

[`words_to_number`]


##### Performance Optimization
- Checking for valid dictionary words Using Trie Data structure.
- Trie data is populated and stored as a `Global Constant`. This avoids re-computation (dictionary file read and Trie populate) between multiple functions, and will save considerable time if dictionary file is larger.
- When doing Graph search, if valid prefix of a dictionary word is Not formed, the graph search is pre-maturely discontinued at that stage.

##### Assumptions
Assumptions Made in this program
- There are many words in the dictionary which are NOT Useful (yo, ey, si, fr) and Needs data cleaning.

- The Approach currently considers only maximum of combination of two words together, though it can be extended for more words.

##### Data structures and libraries used

The VanityNumber module uses Most Popular 20,000 words in a [dictionary_20k.txt] taken from [google-10000-english](https://github.com/first20hours/google-10000-english)

It uses the following Libraries for Data Structure:
- [pygtrie](https://github.com/google/pygtrie) - Python library implementing a trie data structure, for checking valid dictionary word.

- [heapq](https://docs.python.org/3.7/library/heapq.html) - Python library for implementing a Min Heap Priority Queue, for returning top N nodes.

- [deque](https://docs.python.org/3.7/library/collections.html) - Deque for implementing a Queue Data-structure for Breadth first graph search
