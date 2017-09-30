# tornado_sync_log_demo
一个关于tornado异步情况下日志混乱的解决方案   
A solution to tornado asynchronous log chaos...

# Environment
```
python==2.7.10
tornado==4.2
```

##  Server
```
python main.py --port=8888
```

## Client
```
cd demo
python demo.py
```

## Result:
```
#########Create a global logger#########
2017-09-30 13:04:58,588-monitor-demo.<module>.24 - ERROR - the first line
2017-09-30 13:04:58,588-monitor-demo.<module>.24 - ERROR - the second line...
```
