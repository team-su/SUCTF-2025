1. 
```bash
docker build -t "jit16" . 
```

2. 
```bash
docker run -d -p "0.0.0.0:19198:8888" -h "jit16" --name="jit16" jit16doc
```
