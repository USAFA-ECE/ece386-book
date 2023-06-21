# 08 - Linear Algebra and GPUs

## Pre-Reading

- [Explainer: What Are Tensor Cores? | TechSpot](https://www.techspot.com/article/2049-what-are-tensor-cores/)

### Objectives

- Discuss why linear algebra and GPUs are the bedrock of machine learning.
- Explain how GPU hardware accelerates mathematic computations.
- Describe the difference between memory- and math-limited algorithms.

## Linear Algebra

With NVIDIA recently becoming the [seventh company ever to hit $1 trillion market-cap](https://www.marketwatch.com/story/nvidia-officially-closes-in-1-trillion-territory-becoming-seventh-u-s-company-to-hit-market-cap-milestone-88ead8f9) and the boom of AI, it is clear that GPUs are a critical hardware. But what are they and what do they actually do for AI computation?

**Answer:** The vast majority of modern machine learning is handled with linear algebra and a little bit of calculus.

### Vectors and Matrices

> [3Blue1Brown - Vectors, what even are they?](https://www.3blue1brown.com/lessons/vectors)

- In physics, and related engineering, a vector is thought of as an arrow pointing in space; it has magnitude and direction.
- In computer science, a vector - or array - is an ordered list, where each element corresponds with an attribute.
- Mathematicians generalize this to say that vectors can be multiplied by each other and added to a scalar.

A matrix is similar to a vector, but has two dimensions always expressed as **rows** then **columns**. A 2x3 matrix has two rows and three columns.

#### Dot Products

A dot product is essentially how well two sets of numbers align with each other. A dot product with a small magnitude means little alignment, while a large magnitude means more alignment.

When you open a door you push near the knob because that gives you good alignment between the force on the door and the motion of the door. Mathematically, this is a large dot product.
If you try to open a door by pushing near the hinge then there is poor alignment between the force and motion. This is a small dot product, and it is very difficult to get the door to swing!

The dot product can be calculated as either the product of the magnitudes (lengths) of each vector and the cosine of the angel between them. Visually, this is the transformation of two arrows in space.

$$a \cdot b = |a|\cdot|b|\cdot\cos(\theta)$$

Alternatively, the dot product can be calculated as the multiplication and summation of each element of two matrices. This formation will be more helpful for understanding the application to machine learning.

$$\mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^{n} a_i b_i$$

#### Matrix Multiplication

Two matrices can be multiplied together. The multiplication of an $m\times n$ matrix with an $n \times p$ matrix will be an $m \times p$ matrix. Notice that the inner, $n$, dimensions must match in order for a dot product to be possible.

### Neural Networks

A neural network is a system of interconnected neurons inspired by the function of the human brain. The neurons exist in three types of layers:

1. **Input layer** takes the sample as a vector
2. **Hidden layers** handle the work of extracting features from the sample
3. **Output layer** provides probabilities that a sample belongs to a particular class

The neurons in each layer are linked through a series of connections, each of which is assigned a specific weight. The weight of a link from one neuron to the next signifies the importance of the first neuron to the neuron in the next layer.

When conducting inference, the input layer will take in values. To determine the value of each neuron in the next layer, the network multiplies each input value by the corresponding weight and then adds up these products. This is known as the *weighted sum*. If the incoming values are represented as a vector $V$ and the connection weights are represented as a vector $W$ then the weighted sum at a neuron $N$ is the dot product of the two vectors. In addition to the weights associated with the connections, each neuron in the network possesses an additional parameter known as a *bias*, $B$. The bias allows for adjusting the output of the neuron along with the weighted sum. Thus, the final value of a neuron is:
$$N = (\vec{V} \cdot \vec{W}) + B$$
Once the total of the weighted sum and the bias crosses a particular threshold, the neuron becomes *activated*. There are numerous activation functions; two common ones are rectified linear unit ([ReLU](https://builtin.com/machine-learning/relu-activation-function)) and sigmoid.

Overall, the interaction between weights, biases, and activation functions allows neural networks to learn complex patterns and make informed predictions.

#### TensorFlow

In mathematics, a *tensor* is an algebraic object that describes multilinear relationships between sets of other algebraic objects related to a vector space.

[TensorFlow](https://www.tensorflow.org/about) is an open source end-to-end machine learning platform developed by Google. It constrains the definition of tensors in [Introduction to Tensors](https://www.tensorflow.org/guide/tensor): **tensors are multi-dimensional arrays with a uniform type.**

TensorFlow uses tensors to construct neural networks.

Matricies and vectors are subsets of tensors, so matrix multiplication and dot products are common operations on tensors as well. TensorFlow makes extensive use of elementwise multiplication and summation during both training and inference.

## Graphics Processing Units

> [GPU Performance Background User's Guide - NVIDIA Docs](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html)

NVIDIA GPUs consist of a number of Streaming Multiprocessors (SM), on-chip L2 cache, and high-bandwidth DRAM. Arithmetic and other instructions are executed by the SMs; data and code are accessed from DRAM via the L2 cache. Each SM has its own instruction schedulers and various instruction execution pipelines.

![Simplified view of the GPU architecture](https://docscontent.nvidia.com/dita/00000186-1a08-d34f-a596-3f291b140000/deeplearning/performance/dl-performance-gpu-background/graphics/simple-gpu-arch.svg)

**Multiply-add is the most frequent operation in modern neural networks**, acting as a building block for fully-connected and convolutional layers, both of which **can be viewed as a collection of vector dot-products**.

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

US based [NVIDIA](https://www.nvidia.com/en-us/about-nvidia/) is the world leader in GPU design. They are fabless, meaning they design chips but do not make them themselves. Currently Taiwan Semiconductor Manufacturing Co. (TSMC) [makes the bulk of NVIDIA chips](https://www.reuters.com/business/nvidia-ceo-says-interested-exploring-chip-manufacturing-with-intel-2022-03-23/).

Two critical NVIDIA technologies are CUDA Cores and Tensor Cores

#### CUDA Cores

[An Even Easier Introduction to CUDA | NVIDIA Technical Blog](https://developer.nvidia.com/blog/even-easier-introduction-cuda/)

**CUDA** is an API that allows softare to directly access NVIDIA GPU instruction set. The CUDA Toolkit allows developers to use C++ to interact with the cores, but many libraries - such as TensorFlow - have implmented CUDA under the hood.

CUDA is used in numerous applications, from scientific computing to gaming.

#### Tensor Cores

Tensor Cores were introduced in the NVIDIA Volta™ GPU architecture to accelerate matrix multiply-add operations for machine learning and scientific applications.

- These instructions operate on small matrix blocks (for example, 4x4 blocks).
- These smaller matrix blocks are then aggregated.
- Tensor Cores can compute and accumulate products in higher precision than the inputs. For example, during training with FP16 inputs, Tensor Cores can compute products without loss of precision and accumulate in FP32.
- When math operations cannot be formulated in terms of matrix blocks - for example, element-wise addition - they are executed in CUDA cores.
- Effeciency is best when matrix dimensions are multiples of 16 bytes.

Tenosr Cores continue to be improved with additional supported data types in the Turing Architecture.

### Performance

Performance of a function on a given processor is limited by one of the following three factors; **memory bandwidth, math bandwidth and latency**.

- In cases of insuffecient parallelism, latency will be the greatest limiting factor.
- If there is suffecient parallelism, math or memory will be the greatest limiting factor, based on specific arithmetic intensity of the algorithm and the math vs. memory bandwidth of the processor.

#### Math vs. Memory Bandwidth

How much time is spent in memory or math operations depends on both the algorithm and its implementation, as well as the processor’s bandwidths.

- **arithmetic intensity** is the ratio of the number of mathematical operations vs. the number of bytes accessed.
- the **ops:byte ratio** is the ratio of math bandwidth vs. memory bandwidth for a given processor.
- an algorithim is **math limited** on a given processor if the arithmetic intesity is higher than  the processor's ops:byte ratio.
- an algorithim is **memory limited** on  a given processor if the arithmetic intensity is lower than the processor's ops:byte ratio.

#### DNN Operation Performance

Modern deep neural networks are built from a variety of layers, who's operations fall into three categories.

1. **Elementwise operations** are independent of all other elements within the tensor. Examples include summation or ReLU. These tend to be *memory-limited.*
2. **Reduction operations** produce values computed over a range of input tensor values, to include pooling, batch normalization, or computing means. These tend to be *memory- limited.*
3. **Dot-Product Operations** typically involve a weight tensor and an activation tensor. In the case of fully-connected layers, these dot products are typically expressed as matrix-matrix. These may be *math-limited if the matricies are large enough,* otherwise they are memory-limited.

## Conclusion

The execution of linear algebra on GPUs is foundational to modern machine learning. Linear algebra provides the mathematical framework that underpins many machine learning algorithms. Neural networks, in particular, are heavily reliant on using weighted sums dot products to propagate information and adjust weights through the network layers.

Graphics Processing Units (GPUs) with their highly parallelized structures have revolutionized the computational efficiency of these operations. Technologies like NVIDIA's CUDA and Tensor Cores allow for the optimized execution of the matrix and vector operations that are so common in machine learning, significantly accelerating the training and inference processes of deep learning models.

Understanding the performance dynamics of these GPUs—such as memory bandwidth, math bandwidth, and latency—allows for the optimized implementation of algorithms. Deep neural networks often need to be carefully designed and tuned to effectively leverage the computational capabilities of GPUs.

In essence, the interplay of linear algebra and GPU technology forms the bedrock of contemporary machine learning, enabling the creation and operation of complex models that can learn from and make predictions on vast amounts of data.
