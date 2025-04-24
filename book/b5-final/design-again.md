# Final: Design Again Checkpoint

Now that you have completed a few components, you probably need to iterate on your initial design!

## Deliverables

1. Update your initial design diagram.
2. Make a *detailed* flow diagram of the python script that is running in the Docker container on your Jetson.
3. Submit to Gradescope

### Software Flow Charts

Recall the following basic shapes for software flow charts:

**Oval** is the start or end

```mermaid
flowchart LR
    id1([docker run ... python app.py])
```

**Rectangle** is a process

```mermaid
flowchart LR
    id1[Init Whisper pipeline]
```

**Diamond** is a decision

```mermaid
flowchart LR
    id1{Rising edge?}
```

**Parallelogram** is input/output

```mermaid
flowchart TD
    id1[/GPIO Pin 29/]
```

There are many other symbols, for example **cloud** to represent a cloud hosted server.

```mermaid
architecture-beta
    service cloud(cloud)[wttrin]
```
