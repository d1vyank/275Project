275Project
==========

Proposal:

An application to pull web browsing history for a day from a browser and create a graph linking all the websites to each other(a webpage is a vertex and links to each other are edges). Links can be found be found by parsing an HTML page and searching the page. The graph will be displayed using a visualisation library like graphviz.

We also plan to add options to view alternate paths between webpages.

Milestones:
1.) Extract browser history to a csv file and create graph vertices
2.) Figure out the HTML parsing library usage and implement searching algorithm to find paths and add edges.
(We will use memoization to store webpages locally so that they are not loaded more than once)
3.) Graphically display all the data stored above
4.) Write algoritm to find alternate paths between edges


By: Divyank Katira
    Edmond Chui
