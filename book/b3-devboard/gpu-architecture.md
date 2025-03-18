# GPU Architecture

## Pre-Reading

- [GPU Performance Background User's Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html)

![Spiderman with and without Ray Tracing](https://i.ytimg.com/vi/yBDJvYgIRRs/maxresdefault.jpg)

### Objectives

- Explain how GPU hardware accelerates mathematic computations.
- Describe the difference between memory- and math-limited algorithms.

## Accumulating your Multiply Accumulates

> Multiply-add is the most frequent operation in modern neural networks, acting as a building block for fully-connected and convolutional layers, both of which can be viewed as a collection of vector dot-products.
> ~ [GPU Performance Background User's Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html)

Recall that a dot product can be calculated as the product of the magnitudes (lengths) of each vector and the cosine of the angel between them.
Visually, this is the transformation of two arrows in space.

$$
c = \mathbf{a} \cdot \mathbf{b} = |\mathbf{a}|\cdot|\mathbf{b}|\cdot\cos(\theta)
$$

Alternatively, the dot product can be calculated as the multiplication and summation of each element of two matrices.
This formation will be more helpful for understanding the application to machine learning.

$$
c= \bf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i
$$

As we've seen in previous exercises, a for loop that iterates element-wise over the vectors is *extremely* slow.
**But** these operations can happen in parallel, via *matrix multiplication*.

The multiplication of an $m\times n$ matrix with an $n \times p$ matrix will be an $m \times p$ matrix.
Notice that the inner, $n$, dimensions must match in order for a dot product to be possible.

$$
\mathbf{C} = \mathbf{A} \mathbf{B}, \quad \text{where} \quad C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}

$$

### Tensors in Neural Networks

Recall that tensors are multi-dimensional matricies and that DNNs operate on tensors via three types of layers:

1. **Input layer** accepts a batch of samples, where each sample is an N-dimension tensor of data.
2. **Hidden layers** handle the work of extracting features from each sample.
3. **Output layer** provides probabilities that a sample belongs to a particular class.

The neurons in each layer are linked through a series of connections, each of which is assigned a specific weight. The weight of a link from one neuron to the next signifies the importance of the first neuron to the neuron in the next layer.

When conducting inference, the input layer will take in values. To determine the value of each neuron in the next layer, the network multiplies each input value by the corresponding weight and then adds up these products. This is known as the *weighted sum*. If the incoming values are represented as a vector $V$ and the connection weights are represented as a vector $W$ then the weighted sum at a neuron $N$ is the dot product of the two vectors. In addition to the weights associated with the connections, each neuron in the network possesses an additional parameter known as a *bias*, $B$. The bias allows for adjusting the output of the neuron along with the weighted sum. Thus, the final value of a neuron is:

$$
N = (\mathbf{V} \cdot \mathbf{W}) + B
$$

Once the total of the weighted sum and the bias crosses a particular threshold, the neuron becomes *activated*. There are numerous activation functions; two common ones are rectified linear unit ([ReLU](https://builtin.com/machine-learning/relu-activation-function)) and sigmoid.

Overall, the interaction between weights, biases, and activation functions allows neural networks to learn complex patterns and make informed predictions.

## Graphics Processing Units

> The GPU is a highly parallel processor architecture, composed of processing elements and a memory hierarchy. At a high level, NVIDIA® GPUs consist of a number of Streaming Multiprocessors (SMs), on-chip L2 cache, and high-bandwidth DRAM. Arithmetic and other instructions are executed by the SMs; data and code are accessed from DRAM via the L2 cache.
> ~ [GPU Performance Background User's Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html)

![Simplified view of the GPU architecture](https://docscontent.nvidia.com/dita/00000186-1a08-d34f-a596-3f291b140000/deeplearning/performance/dl-performance-gpu-background/graphics/simple-gpu-arch.svg)

### GPU Execution

- GPUs execute many threads concurrently.
- GPUs execute functions using a 2-level hierarchy of threads. A given function’s threads are grouped into equally-sized *thread blocks*, and a set of thread blocks are launched to execute the function.
- GPUs hide dependent instruction latency by switching to the execution of other threads. Thus, the number of threads needed to effectively utilize a GPU is much higher than the number of cores or instruction pipelines.
- At runtime, a block of threads is placed on an SM for execution, enabling all threads in a thread block to communicate and synchronize efficiently.

![Utilization of an 8-SM GPU when 12 thread blocks with an occupancy of 1 block/SM at a time are launched for execution. Here, the thread blocks execute in 2 waves, the first wave utilizes 100% of the GPU, while the 2nd wave utilizes only 50%.](https://docscontent.nvidia.com/dita/00000186-1a08-d34f-a596-3f291b140000/deeplearning/performance/dl-performance-gpu-background/graphics/utilize-8sm-gpu.svg)

#### General Matrix Multiplication

GPUs implement general matrix multiplication ([GEMM](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html#gpu-imple)) by partitioning the output matrix into tiles, which are then assigned to thread blocks.

Each thread block computes its output tile by stepping through the K dimension in tiles, loading the required values from the A and B matrices, and multiplying and accumulating them into the output C matrix.
![Tiled outer product approach to GEMMs](https://docscontent.nvidia.com/dita/00000186-1a08-d34f-a596-3f291b140000/deeplearning/performance/dl-performance-matrix-multiplication/graphics/tiled-outer-prod.svg)

### NVIDIA GPUs

US based [NVIDIA](https://www.nvidia.com/en-us/about-nvidia/) is the world leader in GPU design.
They are fabless, meaning they design chips but do not make them themselves.
Taiwan Semiconductor Manufacturing Co. (TSMC) makes the bulk of NVIDIA chips.

Two critical NVIDIA technologies are CUDA Cores and Tensor Cores

#### CUDA Cores

**CUDA** is an API that allows software to directly access NVIDIA GPU instruction set.
The CUDA Toolkit allows developers to use C++ to interact with the cores, but many libraries - such as TensorFlow and PyTorch - have implemented CUDA under the hood.

See [An Even Easier Introduction to CUDA | NVIDIA Technical Blog](https://developer.nvidia.com/blog/even-easier-introduction-cuda/) if you really want to explore using C++ to crate a massively parallel application.

#### Tensor Cores

Tensor Cores were introduced in the NVIDIA Volta™ GPU architecture to accelerate matrix multiply-add operations for machine learning and scientific applications.

- These instructions operate on small matrix blocks (for example, 4x4 blocks).
- These smaller matrix blocks are then aggregated.
- Tensor Cores can compute and accumulate products in higher precision than the inputs. For example, during training with FP16 inputs, Tensor Cores can compute products without loss of precision and accumulate in FP32.
- When math operations cannot be formulated in terms of matrix blocks - for example, element-wise addition - they are executed in CUDA cores.
- Efficiency is best when matrix dimensions are multiples of 16 bytes.

Tenosr Cores continue to be improved with additional supported data types in the Turing Architecture and now Ada Architecture.

### PCIe

Peripheral Component Interconnect Express (PCIe) is the connection GPUs use to connect to your computer.

The [NVIDIA RTX 5000 Ada GPU](https://www.nvidia.com/en-us/design-visualization/rtx-5000/) has PCIe Gen4 x16,
meaning there are 16 lanes of parallel data transfer according to the fourth generation protocol...
this gets bandwidth of about 64 GB/s, assuming your CPU can keep up!

```{figure} https://docscontent.nvidia.com/dims4/default/0987ede/2147483647/strip/true/crop/1099x727+0+0/resize/2198x1454!/format/webp/quality/90/?url=https%3A%2F%2Fk3-prod-nvidia-docs.s3.us-west-2.amazonaws.com%2Fbrightspot%2Fconfluence%2F00000195-8599-dbb9-a9bf-b5fbe68d0000%2Fimages%2Fdownload%2Fattachments%2F2487214394%2Fimage2020-10-19_19-41-1-version-1-modificationdate-1669944867740-api-v2.png


NVIDIA PCIe Interface shown by circle **3**
```

## GPU Performance

Performance of a function on a given processor is limited by one of the following three factors; **memory bandwidth, math bandwidth and latency**.

- In cases of insufficient parallelism, latency will be the greatest limiting factor.
- If there is sufficient parallelism, math or memory will be the greatest limiting factor, based on specific arithmetic intensity of the algorithm and the math vs. memory bandwidth of the processor.

How much time is spent in memory or math operations depends on both the algorithm and its implementation, as well as the processor’s bandwidths.

- **arithmetic intensity** is the ratio of the number of mathematical operations vs. the number of bytes accessed.
- the **ops:byte ratio** is the ratio of math bandwidth vs. memory bandwidth for a given processor.
- an algorithm is **math limited** on a given processor if the arithmetic intesity is higher than  the processor's ops:byte ratio.
- an algorithm is **memory limited** on  a given processor if the arithmetic intensity is lower than the processor's ops:byte ratio.

### DNN Performance

Modern deep neural networks are built from a variety of layers, who's operations fall into three categories.

1. **Elementwise operations** are independent of all other elements within the tensor. Examples include summation or ReLU. These tend to be *memory-limited.*
2. **Reduction operations** produce values computed over a range of input tensor values, to include pooling, batch normalization, or computing means. These tend to be *memory- limited.*
3. **Dot-Product Operations** typically involve a weight tensor and an activation tensor. In the case of fully-connected layers, these dot products are typically expressed as matrix-matrix. These may be *math-limited if the matricies are large enough,* otherwise they are memory-limited.

## Conclusion

The execution of linear algebra on GPUs is foundational to modern machine learning. Linear algebra provides the mathematical framework that underpins many machine learning algorithms. Neural networks, in particular, are heavily reliant on using weighted sums dot products to propagate information and adjust weights through the network layers.

Graphics Processing Units (GPUs) with their highly parallelized structures have revolutionized the computational efficiency of these operations. Technologies like NVIDIA's CUDA and Tensor Cores allow for the optimized execution of the matrix and vector operations that are so common in machine learning, significantly accelerating the training and inference processes of deep learning models.

Understanding the performance dynamics of these GPUs—such as memory bandwidth, math bandwidth, and latency—allows for the optimized implementation of algorithms. Deep neural networks often need to be carefully designed and tuned to effectively leverage the computational capabilities of GPUs.

In essence, the interplay of linear algebra and GPU technology forms the bedrock of contemporary machine learning, enabling the creation and operation of complex models that can learn from and make predictions on vast amounts of data.
