# Restore this prepared repository with its real history

The ZIP includes the source files and takemeter-history.bundle. The bundle preserves
the original starter history plus one genuine preparation commit. It does not claim
that four Unit 5 milestones or the student's criteria have been completed.

After extracting the ZIP, run this from its parent directory:

```bash
git clone TakeMeter_Unit5/takemeter-history.bundle takemeter
cd takemeter
git remote rename origin archive
```

Fork https://github.com/codepath/ai201-project3-takemeter-starter-v2026 on GitHub.
Use the fork you will submit again in Unit 6. Add that actual fork as origin:

```bash
git remote add origin https://github.com/YOUR-USERNAME/ai201-project3-takemeter-starter-v2026.git
```

Before your own commits, set your own name and email. No email has been invented.
Complete and commit the actual reading/taxonomy decisions, then your five criteria,
then your reviewed labels before training. Commit the notebook's actual output files
after training. Use git log to verify that the criteria commit comes first.

```bash
git push -u origin main
```

The ZIP excludes the virtual environment and model cache because those are machine
specific. Recreate .venv using RUNNING.md; install ipykernel too if your editor needs
a Jupyter kernel. The environment-check evidence describes the assistant's runtime,
not a replacement for running test.py on your machine.
