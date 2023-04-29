## Staticfiles
django on Prod need whitenoise  
[link zur Doc](https://whitenoise.readthedocs.io/en/stable/changelog.html#v4-0)
```
pip install whitenoise
```
## Export all .env.dev files for Project

[link zur doc](https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs)
**94 I found the most efficient way is**
 ```
 export $(xargs < .env)
 ``` 


## Set localtime to host-time
[link zur doc](https://stackoverflow.com/questions/24551592/how-to-make-sure-dockers-time-syncs-with-that-of-the-host)

```
/etc/localtime:/etc/localtime:ro
```