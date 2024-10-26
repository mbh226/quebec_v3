## How to contribute to Quebec

#### Git Basics

The Quebec team follows the standard git workflow to manage this repository. Beginners will find the steps detailed below helpful in making their first contributions.

1. Clone Repository

```
git clone https://github.com/kgp33/quebec_v2.git
```

2. Move to repository directory 

```
cd quebec_v2
```

3. Check status and confirm its up to date.

```
git status
```

4. Create a new branch.

```
git checkout -b <new branch>
```

5. Check that you're working in the newly created branch.

```
git branch
```

The branch your working on will be marked with an asterisk.

6. Add a new file or make changes to an existing file using VSCode or preferred editor.

7. Stage file for next commit.

```
git add <filename>
```
8. Commit changes with descriptive message.

```
git commit -m "Added new file and this is my descriptive message."
```

9. Push changes to repository branch.

```
git push origin <branch you created in step 4>
```

#### SecDevOps Approach
The Quebec team has agreed to take a SecDevOps approach to our project's development and all contributors are expected to do the same. SecDevOps is a software development approach that prioritizes security.[^1] All contributors must abide by Quebec's Secure Coding Standard.

[^1]: https://www.pluralsight.com/blog/software-development/secdevops#:~:text=with%20Pluralsight%20Flow-,What%20is%20SecDevOps?,vulnerabilities%20they%20missed%20earlier%20on
