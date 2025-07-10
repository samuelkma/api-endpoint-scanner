summer 2025 


Default wordlist (common.txt) is from Daniel Miessler (Github) 's api-endpoints-res.txt (SecLists repo).

The defualt container will be built upon the common.txt from Daniel Miessler (12k keywords), and we will have additional keyword .txt files that are more narrowed down depending on the type of server (in the future). Thus, instead of having to manually rebuild the container every single time we wish to run a different list, we can instead change the -v flag when running through terminal to specify the word list:

(Hypothetical example given of django.txt keyword list, which doesn't exist yet)

docker run --rm \
  -v $(pwd)/data:/app/data \
  api-scanner:dev http://target   --wordlist /app/data/extra/django.txt