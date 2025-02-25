1. 
```bash
docker build -t "pas_sport" . 
```

2. 
```bash
docker run -d -p "0.0.0.0:11451:8888" -h "pas_sport" --name="pas_sport" pas_sport
```

