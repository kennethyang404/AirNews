AirNews
=======
An entirely new bulletin board, an everyone-to-everyone platform for communication.

On Facebook or Twitter, your post can only be seen by your friends or followers, but on this platform, everybody can send messages to anyone else. Built with a weighted-random rank algorithm, this system guarantees that the news with high weight has a greater chance of showing up on first page, but new posts also have a possibility to appear. When users go to the detailed page or click like, weight of the news will increase.

Also, to prevent spam information, a naive bayesian classifier is used.

This platform can be used in many situations. Such as posting college events information or publishing independent news.

Built with JS and Flask on HackCMU 2014


Sample
=======
![Sample](/screenshot.png?raw=true)



Issues
======
Not responsive to different screen sizes
index page can't open when database is empty. When first use, go to /create page to create a new post.


* Web Design: html5up.net
* Bayesian Classifier: https://github.com/codebox/bayesian-classifier
