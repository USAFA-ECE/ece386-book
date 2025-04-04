# Lab 5: Prompt Engineering

## Overview

### Objectives:

1. Engineer a great LLM response with a great prompt.
2. Run an LLM locally with Ollama.
3. Use the **system** role to guide an LLM's response.

### Setup and Deliverables

1. Clone
2. Complete the three tasks below
3. Push everything to GitHub
4. Submit to Gradescope!

## Task 1: Chicago Art Institute API

The [Art Institute of Chicago API](https://api.artic.edu/docs/) is truly splendid!
It's what happens when non-technical institutions invest in technical talent.

For example, you can query and filter their art exhibitions!

Our objective is to **engineer a prompt** to [Claude Sonnet 3.5](https://www.anthropic.com/news/claude-3-5-sonnet),
that *in one go* delivers a Python program for a
multi-step interaction with the Art Institute of Chicago (ArtIC) API *and doesn't need us to edit it!*

```{note}
Sonnet 3.5 is currently freely available for free on [https://claude.ai/](https://claude.ai/new)
up to a quota. But any powerful LLM should be able to do this.
```

### Outcome

Get an entire Python script from Claude that *with no edits* does the following:

1. Accepts a search term from the user.
2. Searches the ArtIC API for exhibitions matching that term and that have artwork titles.
3. Prompts the user for a number of exhibitions they would like to view.
4. Displays the titles of the artwork for those exhibition to the user.
5. Loops until user exit.

### Guidance

To generate this Python script you will need a specific, structured prompt.
Here are some suggestions.

1. Begin the prompt withan overview of what you want and how you are going to ask for it.
    - "I want you to complete some Python code for me. I will first give you background information; then....
    - "The ultimate goal of the script is to...
2. Under the `## Search API Background` subheading, copy *the most* relevant pieces from
    [the docs](https://api.artic.edu/docs/#quick-start) on how the API works.
3. Have another subheading where you copy in background on the [exhibitions](https://api.artic.edu/docs/#exhibitions) endpoint.
4. Finally, provide a `## Python Template` subsection. This should include code in a triple-backtick block.

#### Python Template

I am going to give you [the cadet] the start to the three components that your template should include.
You will need to complete the components and include it in your prompt.

**Start** by guiding the LLM to use the libraries you want.
For example we want the Requests library instead of the builtin HTTP library.

```python
import requests
```

**Next**, provide the function definitions that you think you will need.
If you aren't sure what these need to be *draw a block diagram of how you think the program should flow!*
Each `def` must:

1. Have a descriptive name
2. Use type-hints in the parameters and return field
3. Have `'''Block comments'''` that state what the function should do.

Example:

```python
def search_exhibitions(term: str) -> list[int]:
    '''Make a request to exhibitions/search for the search term,
    using Elasticsearch `exists` option to only return results where the `artwork_titles` field is not empty
    Process the result and return a list of exhibitions IDs.
    '''
```

**Finally**, provide guidance on the TODO to make the `main()` method.
Here is the start of how that might look.

```python
# TODO: main function that repeatedly prompts the user...
```

### Deliverables

After Claude generates your script, paste it into `ArtIC/exhibition_explorer.py`,
run `black` on it, install `ArtIC/requirements.txt` into your virtual environment,
and run the script to see how it does!

Once you have a working script:

- Complete the `ArtIC/README.md`
- Ensure `ArtIC/exhibition_explorer.py` is complete
- Commit and push to GitHub

## Task 2: Running an LLM Locally

You can do this on any computer that has Docker or Podman!

```{warning}
You *can* get the GPU on the Jetson running Ollama.
But it took Capt Yarbrough about 20 hours to figure out,
so not required for this!

Details below.
```

### Outcome

Talk to an LLM that you are running locally in an Ollama container.

### Guidance

```{tip}
Typing `sudo` is annoying, so you can follow the
[docker post-install steps](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
to not have to type it by adding your user to the `docker` group.
```

Make sure you have Docker or Podman installed.

Pull the latest Ollama docker image from [https://hub.docker.com/r/ollama/ollama](https://hub.docker.com/r/ollama/ollama)

```bash
docker pull ollama/ollama
```

Create a volume to cache your Ollama models.

```bash
docker volume create ollama
```

Run the container, mounting the volume, giving it a name, binding a port,
and telling it to serve.

```bash
# The \ and line breaks are just for readability.
docker run -d \
    -v ollama:/root/.ollama/ \
    --name ollama \
    -p 11434:11434 \
    ollama/ollama serve
```

Verify the container is running

```bash
docker ps
```

Optionally, you can hit the API directly

```bash
# Should return "Ollama is running"
curl 127.0.0.1:11434
```

Interact with the container!
The `exec` command takes the name of a container
(`ollama` in our case, set by the `--name` flag above and shown with `docker ps`)
as well as a command `ollama` (but this time means the binary executable)
as well as the subcommand (`help`).
The `-it` flag says to bind to a new interactive terminal.

```bash
docker exec -it ollama ollama help
```

From there, visit the [Ollama Model Library](https://ollama.com/search)
and run one of the smaller models.

### Deliverables

1. Complete `ollama/README.md`

## Task 3: Use the System Role to Guide LLM's Response

# Lab Workday
