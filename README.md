# ECE 386: AI Hardware Applications

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Live website:** [https://usafa-ece.github.io/ai-hardware](https://usafa-ece.github.io/ai-hardware)

Contains all course code and the [Jupyter Book](https://jupyterbook.org/en/stable/intro.html) static website to [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages)
that is automatically built with [GitHub Actions](https://docs.github.com/en/actions).

## Using for class

Browsing the website will show *most* of the content. The Jupyter Notebooks can be easily opened in Google Colab with the launch button :rocket: at the top right of the page.
But there are a few lessons where there is additional code outside of the Jupyter Notebooks. In those instances, you can do any one of the following:

1. Shallow clone of the repository, using the `--depth 1` flag.
2. Fork the repository to your personal account (and periodically fetch updates).
3. Download the relevant files as a zip.

## Contributing to the site

This repository uses the strategy of [Publishing from a branch](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-from-a-branch)
to deploy the static site.

It has two branches:

- `main` which holds the all the Markdown and other files to generate the Jupyter Book. Treat this branch like any other with pushes & pull requests.
- `gh-pages` which is a special branch to GitHub Pages. It is automatically updated with the built HTML files by the Actions. Don't touch this branch!

The book itself is in the `book/` directory. If you change the name of this directory you also must changes it in the `deploy.yml` file.

On every push or pull event to `main` an Action workflow is triggered.
That workflow follows the instructions in `.github/workflows/deploy.yml` to run `jupyter-book build`. After the build creates the HTML files for the static site, the workflow pushes the files to the `gh-pages` branch.

GitHub automatically deploys whatever `index.html` file it finds at the root of `gh-pages` **after** you tell it to do so in settings, see below.

**Modify book content** by making updates to the content in your favorite IDE.
It is as simple as adding/editing the Markdown (`.md`). Jupyter Notebook (`.ipynb`), or Jupyter Book configuration (`.yml`) files and merging to `main`.
No local dependencies needed!

### Preview site before you push

Optionally, if you want to build the site locally, you need to install Jupyter Book.
This requires Python 3.9 or higher, which you should run in a virtual environment.

To use a virtual environment...

```bash
python3 -m venv env
source env/bin/activate
```

Install requirements

```bash
pip install -r requirements-book.txt
```

Make whatever changes you want to the site inside the `book/` directory.

Build the book

```bash
jupyter-book build book/
```

The static files will now be located in `book/_build/`. View the website by opening `index.html` in any browser

```bash
firefox book/_build/index.html
```

You have to rebuild every time you make changes in order to preview them.

Note that `_build/` is in the `.gitignore` file because the actions build what is actually deployed.

Once satisfied, push to `main` and github actions will auto-deploy!
