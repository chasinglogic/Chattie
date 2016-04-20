docker run --name thorin-redis -p 6379:6379 -v /home/mrobinson/data/thorin-redis:/data -d redis redis-server --appendonly yes
