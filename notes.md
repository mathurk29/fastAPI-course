##  Multi-stage builds:
a feature in Docker that allows you to build an image in stages, with each stage represented by a different base image with a different configuration, and each stage capable of passing artifacts (files, directories) to subsequent stages or producing a final image.

This is particularly useful to keep the size of the final Docker image to a minimum by excluding unnecessary files, tools, or libraries that were only required for building the application but not required for running it. It also adds an additional layer of security by removing tools that may expose vulnerabilities.

Here's a basic example of a multi-stage Docker build.

```Dockerfile
# Stage 1: Base image with Python installed, and scripts to build dependencies
FROM python:3.8 as builder

# Setup a directory for the application code
WORKDIR /app

# Copy your application's requirements.txt file
COPY requirements.txt .

# Install your Python dependencies
RUN pip install -r requirements.txt


# Stage 2: An image to run the application
FROM python:3.8-slim

# Copy the virtual environment from the builder stage
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

# Copy the application code
WORKDIR /app
COPY . .

# Set up necessary environment variables
ENV PATH="/scripts:${PATH}"

# Your run command
CMD ["python", "app.py"]
```

In the above Dockerfile, we first define a stage using `python:3.8` as base image and install the application requirements. This stage is named `builder` (names are assigned to stages using `as <name>`).

Then a second stage is created using a more slim Python image (`python:3.8-slim`). The necessary files from the `builder` stage are copied to this stage using the `COPY --from=builder` command. Then the application code is copied and the image is set up to run the app.

The final image does not contain any unnecessary files or tools that are present in the builder stage, keeping the image size small and more secure.

You can add any number of stages depending on your requirements. This is a very powerful feature and can be used in creative ways to build advanced Docker images. It's particularly popular for compiled languages (like Go, C++, Java, etc.) but can also be used effectively with Python and other interpreted languages.


Example:

```
# syntax=docker/dockerfile:1
FROM golang:1.21
WORKDIR /src
COPY <<EOF ./main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

FROM scratch
COPY --from=0 /bin/hello /bin/hello
CMD ["/bin/hello"]
```

The `scratch` image is a special Docker image that is empty. It's not actually provided by any Dockerfile, but is implicitly defined by Docker itself to be a completely empty filesystem. 

Using the `scratch` image is essentially the same as using an empty Dockerfile. It's most common to use `scratch` as a base image when you want to create a Docker image that includes only a statically linked binary executable. 

In your example, it builds a Go executable in one image, then copies the built binary to the `scratch` image in the next stage. That way, the resulting Docker image is kept as small as possible, excluding all the tools and libraries that were only needed for building the binary and would not be necessary to run it.

In `COPY --from=0...`, the `0` refers to the first build stage (the one building the Go binary). The stages are indexed starting from 0. If you had labelled your build stages with `as` like `FROM ... as builder` in the first stage, you could also refer to it with the label like: `COPY --from=builder...`. 

Then, when running a container with this image, it executes this binary with `CMD ["/bin/hello"]`.
That's all the resulting Docker image does – running the Go binary, nothing more, so the resulting Docker image size is as small as it can be.