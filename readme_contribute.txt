
-------- How to Contribute ------------
We follow standard lightweight commit process.
Reference: https://guides.github.com/introduction/flow/

Please regress before creating a pull request.  This assumes we have tests.

-------- Workflow - How to create a "pull request" --------------
Reference: https://www.thinkful.com/learn/github-pull-request-tutorial/Time-to-Submit-Your-First-PR

The following assumes you did a 'git clone' to populate a local workarea, worked for a while and now decide you want to commit your changes to the original repository.  As such you are starting with 2 repositories which I will call "local" and a remote "upstream".

To create a pull request you need to persist your changes somewhere.  To do this you create yet a third repository which is a second remote called "mygithub" on your github account. You issue the pull request from that account.


Diagram:
                          3,4=fork
                         --------->
        github:metrowest  9=pullreq    github:yourname
        "origin"         <---------    "mygithub"
            \                         /
             \                       /
      1=clone \                     / 8=push mygithub
               \                   /
                local repository
                   2=edit and commit to main
                   5=set remotes
                   6=branch
                   7=commit to branch
                    
                    

Steps:

1) Clone the project you're interested in (metrowest) to a local repository

2) Make changes and commit your changes to the local repository.  You didn't make a branch so you're working on main - this is a common scenario.
git add *
git commit

3) Realize OMG - you fixed something and want to share it with the original author.  You need to create a pull request...

4) Go to the github web page of the original project - use the "fork" button.  This creates a repository in YOUR github web page - this will be the "mygithub" repository.

5) In your local workarea -  create remotes for "mygithub".  You already have "origin"
git remote -v  (just to see refrence to "origin" - the metrowest github)
git remote add mygithub https://github.com/YOURNAME/REPOSITORY_NAME
git remote -v  (to see now you have two remotes)

6) In your local workarea - create a branch
git checkout -b MY_BRANCH_NAME   (I typically use something like cwinsor_001_blahblah)
git branch    (just to confirm you are now on the branch)
git merge main (this merges changes from local/main onto your branch)

7) If you make more changes on the branch, "git commit" and they will go on the branch

8) Push to "mygithub" the MY_BRANCH_NAME branch.  This pushes changes to your github on branch. To do this:
Remind yourself:
git branch    (what branch am I on)
git remote -v (what are my remote repositories)
then:
git push mygithub MY_BRANCH_NAME 
You will see
    To https://github.com/cwinsor/kepler.git
    * [new branch]      cwinsor_001_add_setup.py -> cwinsor_001_add_setup.py
You have thus pushed your branch to your github repository.

9) Use your browser and revisit your github repository
Hit the "branches" button
Your branch will show up.  Click on the one associated with the remote repository and push "create pull request".



