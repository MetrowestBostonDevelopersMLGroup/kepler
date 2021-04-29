
### Contribute
We follow standard lightweight commit process.
Refer to https://guides.github.com/introduction/flow/

Please regress before creating a pull request.  This assumes we have tests.


+=====================
Workflow - How to create a "pull request"
https://www.thinkful.com/learn/github-pull-request-tutorial/Time-to-Submit-Your-First-PR

The following assumes you did a 'git clone' to populate a local workarea. You worked for a while and decide you want to commit your changes to the original repository.  As such you are starting with 2 repositories which I will call "local" and "upstream".   To publish your changes as a pull request you will need to create yet a third repository ("origin")

Steps:

1) Clone the project you're interested in (metrowest) to a local repository

2) Edit, add, commit your changes to the local repository.  Regress and repeat as needed :)
git add *
git commit

3) Realize OMG - you fixed something and want to share it with the original author.  You need to create a pull request...

4) Go to the github web page of the original project - use the "fork" button.  This creates a repository in YOUR github web page - this will be the "mygithub" repository.

5) In your local workarea -  create remotes for "upstream" and "mygithub"  - ditch "origin"
git remote -v  (just to see it was referring to the original author's github repository)
git remote add upstream  <whatever the origin was>
git remote add mygithub https://github.com/cwinsor/REPOSITORY_NAME
git remote remove origin
git remote -v  (to see it is now remotes pointing to the two repositories)

6) In your local workarea - create a branch on the local repository
git checkout -b BRANCH_NAME
git branch    (just to show that you are on the branch)
Your changes should be on the branch.

7) 




