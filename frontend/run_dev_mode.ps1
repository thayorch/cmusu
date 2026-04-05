    Write-Host "Building DEV image..."

    docker build -f Dockerfile.dev -t dev .

    Write-Host "Running DEV container..."

docker run -d `
    --name vue-dev `
    -p 5173:5173 `
    -v ${PWD}:/app `
    -v /app/node_modules `
    dev